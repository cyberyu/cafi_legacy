import json
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
    Return: (id, score) if any match is found; otherwise, (-1, -Inf)
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
        return (-1, -Inf)

def text_similarity_score_by_json(index, doc_type, obj_json, **kwargs):
    """
    Find the document most like the given artificial document (json). 
    Example Usage: 
        new_obj_json = text_similarity_score_by_json(index="myindex", doc_type="mytype", obj_json='{"text": "find me"}', fields=['text'], stop_words=[u"is",u"a"])
    Return: a new json object with two extra key "similar_to" and "similarity_score" (which are -1 and -Inf if no match is found) 
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
        r_score = -Inf
    obj_dict["similar_to"] = r_id
    obj_dict["similarity_score"] = r_score
    return json.dumps(obj_dict)

def text_similarity_score_by_content(index, doc_type, content, **kwargs):
    """
    Find the document which is  most like the given content; The optional kwargs will be passed to "more_like_this" query. 
    Example Usage: 
          id, score = text_similarity_score_by_content(index="myindex", doc_type="mytype", content=u"search me", fields=['text'], stop_words=[u"is",u"a"])

    Return: (id, score) if any match is found; otherwise, (-1, -Inf)
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
        return (-1, -Inf)

