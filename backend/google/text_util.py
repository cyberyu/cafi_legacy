import json
from collections import OrderedDict
import numpy as np
from scipy.sparse import coo_matrix
from elasticsearch import Elasticsearch

def _build_default(kwargs):
    """
    build default parameters for ES search; ES default seems not work well for duplication detection. 
    kwargs: dict 
    """
    if not 'max_query_terms' in kwargs:
        kwargs['max_query_terms'] = 4000
    if not 'min_term_freq' in kwargs:
        kwargs['min_term_freq'] = 0
    return 

def index_text(index, doc_type, obj_json, **kwargs):
    """
    Addes or updates the given text(obj_json) into index/doc_type/id. The input obj_json should have "id" and "text"  keys. Other keys in obj_json are left out. 
    """
    es = Elasticsearch()
    obj_dict = json.loads(obj_json)
    id = obj_dict['id']
    text = obj_dict['text']
    body = {"id":id, "text": text}
    es.index(index=index, doc_type=doc_type, id=id, body=body, **kwargs)
    return 

def text_similarity_scores(index, doc_type, **kwargs):
    """
    return a sparse matrix whose (i,j) entry is the similarity score of document i and document j of /index_name/doc_type
    """

    _build_default(kwargs)
    es = Elasticsearch()
    n = es.search(index = index, doc_type = doc_type, body={"query":{"match_all":{}}},search_type="count").get('hits').get('total',0)
    I = []
    J = []
    V = []
    for i in range(n):
        rv = es.mlt(index,doc_type,id=i, **kwargs)
        results = rv['hits']['hits']
        if len(results) > 0: 
            j = int(rv['hits']['hits'][0]['_id'])
            score =  rv['hits']['hits'][0]['_score']
            I.append(i)
            J.append(j)
            V.append(score)
    return coo_matrix((V,(I,J)),shape=(n,n))

def text_similarity_score_by_id(index, doc_type, id, **kwargs):
    """
    Find the document most like the given id  
    Return: (id, score) if any match is found; otherwise, (-1, -np.inf)
    """

    _build_default(kwargs)
    es = Elasticsearch()
    rv = es.mlt(index=index, doc_type=doc_type, id=id, **kwargs)  
    results = rv['hits']['hits']                
    if len(results) > 0:                        
        j = int(rv['hits']['hits'][0]['_id'])   
        score =  rv['hits']['hits'][0]['_score']
        return (j, score)
    else:
        return (-1, -np.inf)

def text_similarity_score_by_json(index, doc_type, obj_json, **kwargs):
    """
    Find the document most like the given artificial document (json). 
    Example Usage: 
        new_obj_json = text_similarity_score_by_json(index="myindex", doc_type="mytype", obj_json='{"text": "find me"}', fields=['text'], stop_words=[u"is",u"a"])
    Return: a new json object with two extra key "similar_to" and "similarity_score" (which are -1 and -np.inf if no match is found) 
    """
    _build_default(kwargs)
    es = Elasticsearch()
    obj_dict = json.loads(obj_json)
    kwargs["docs"] =[{'doc':obj_dict}]   
    body = { 
        "query": {
            "more_like_this": kwargs
            }
        }
    rv = es.search(index=index, doc_type=doc_type, body=body)
    results = rv['hits']['hits']
    if len(results) > 0: 
        r_id = int(results[0]['_id'])
        r_score = results[0]['_score']
    else:
        r_id = -1
        r_score = -np.inf
    obj_dict["similar_to"] = r_id
    obj_dict["similarity_score"] = r_score
    return json.dumps(obj_dict)

def text_similarity_score_by_content(index, doc_type, content, **kwargs):
    """
    Find the document which is  most like the given content; The optional kwargs will be passed to "more_like_this" query. 
    Example Usage: 
          id, score = text_similarity_score_by_content(index="myindex", doc_type="mytype", content=u"search me", fields=['text'], stop_words=[u"is",u"a"])

    Return: (id, score) if any match is found; otherwise, (-1, -np.inf)
    """

    _build_default(kwargs)
    kwargs["like_text"] = content
    es = Elasticsearch()
    body = {
        "query": {
        "more_like_this" : kwargs 
        }
    }     
    rv = es.search(index=index, doc_type=doc_type, body=body)
    results = rv['hits']['hits']
    if len(results) > 0: 
        return (int(results[0]['_id']),  results[0]['_score'])
    else:
        return (-1, -np.inf)

class _Graph:
    """
    A helper class for grouping (by finding connected components of undirected graph) 
    """
    def __init__(self):
        self._adjacent={}
        self.n_components = 0
    def add_vertex(self,v):
        if not v in self._adjacent: 
            self._adjacent[v] = set()
        return 

    def add_edge(self, v1, v2):
        self._adjacent[v1].add(v2)
        self._adjacent[v2].add(v1)
        return 
    
    def find_components(self):
        self._color = {v:0 for v in self._adjacent}
        cur_comp = 0 
        for v in self._adjacent:
            if self._color[v] == 0:
                cur_comp += 1
                self.dfs(v, cur_comp)
        self.n_components = cur_comp
        r_l = [[k for k,v in self._color.iteritems() if v == i] for i in range(1,self.n_components+1)]
        return r_l
    
    def dfs(self, s, cur_comp):
        self._color[s] = cur_comp
        for w in self._adjacent[s]:
            if self._color[w] == 0 : 
                self.dfs(w,cur_comp)
        return 

def text_grouping_by_graph_cut(docs, threshold):
    """
    Group similar docs based on similarity scores. Similarity score greater than the threshold means two docs are duplicates. 
    Input docs: a list(json) of docs. Each doc has fields "id", "similar_to", "similarity_score", "rank".  
    Return: a OrderedDict {doc_repr:[doc, doc, ...], doc_repr:[doc,doc,...]} where each item is a group; doc_repr is a representative of a group. The OrderedDict is sorted by doc_repr's rank
    """
    g = _Graph()
    docs = json.loads(docs)
    for doc in docs:
        id0 = doc['id']
        g.add_vertex(id0)
        id1 = doc["similar_to"] 
        score = doc["similarity_score"]
        if id1 != -1 and score >= threshold: 
            g.add_vertex(id1)
            g.add_edge(id0, id1)
    groups_ids = g.find_components()
    t = {}
    for group in groups_ids:
        min_id = min(group, key=lambda x: docs[x]['rank'])
        group.remove(min_id)
        t[min_id] = group
    return OrderedDict(sorted(t.items(),key=lambda x: docs[x[0]]['rank']))

    
    
