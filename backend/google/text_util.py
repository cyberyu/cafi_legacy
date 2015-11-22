import json
from collections import OrderedDict
import numpy as np
from scipy.sparse import coo_matrix
from elasticsearch import Elasticsearch
import networkx as nx
import community

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
            },
        "size": 10
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

# author = __shyu__

        # this function will create a document clustering map for all documents asserted into elastic search
        #  searchsize is the number of documents to be compared, min = 1, max = 10
        #  cutv is the threshold of cutting the Elastic search score
        #  Outputting a dictinary, which can resolve all document similarity via simple json loop
        #  Sample output {u'56': [u'11', 0.0], u'54': [u'20', 0.66334870000000001], u'28': [u'4', 0.0],
        # u'22': [u'4', 0.0], u'29': [u'9', 0.0], u'49': [u'30', 0.0], u'52': [u'5', 0.0], u'53': [u'4', 0.0],
        # u'24': [u'24', 1], u'25': [u'11', 0.0], u'26': [u'5', 0.0], u'27': [u'5', 0.0], u'20': [u'20', 1],
        # u'21': [u'4', 0.0], u'48': [u'30', 0.0], u'23': [u'16', 0.0], u'46': [u'9', 0.0], u'47': [u'30', 0.0],
        # u'44': [u'9', 0.0], u'45': [u'9', 0.0], u'42': [u'16', 0.0], u'43': [u'30', 0.0], u'40': [u'11', 0.0],
        # u'41': [u'11', 0.58372170000000001], u'1': [u'16', 0.0], u'0': [u'4', 0.0], u'3': [u'9', 0.0],
        # u'2': [u'4', 0.0], u'5': [u'5', 1], u'4': [u'4', 1], u'7': [u'16', 0.0], u'6': [u'24', 0.0], u'9': [u'9', 1],
        # u'8': [u'11', 0.0], u'51': [u'24', 0.0], u'39': [u'30', 0.0], u'38': [u'16', 0.0], u'59': [u'4', 0.0],
        # u'58': [u'9', 0.0], u'11': [u'11', 1], u'10': [u'16', 0.0], u'13': [u'5', 0.0], u'12': [u'16', 0.0],
        # u'15': [u'5', 0.0], u'14': [u'4', 0.0], u'17': [u'30', 0.0], u'16': [u'16', 1], u'19': [u'9', 0.0],
        # u'18': [u'11', 0.0], u'31': [u'9', 0.67990790000000001], u'30': [u'30', 1], u'37': [u'24', 0.0],
        # u'36': [u'30', 0.67351369999999999], u'35': [u'4', 0.0], u'34': [u'16', 0.0], u'33': [u'24', 0.0],
        # u'55': [u'16', 0.0], u'32': [u'11', 0.69575894000000005], u'57': [u'5', 0.0], u'50': [u'4', 0.0]}
        # where the keys are document id,  the values are list of "similarto document" id and score
        # The similar to document is determined by their degrees in the graph
        # The clustering is based on Louvain Modularity, Ref. "The Louvain method for community detection in large networks" invented by Vincent Blondel
        # Usage: using larger searchsize and smaller cutv value will result in well-connected graph, resulting in small number of large document clusters.
        # Incontrast, using small searchsize and large cutv value will result in disconnected graph, yielding large number of small document clusters


def text_similarity_clustering(index, doc_type, searchsize, cutv, **kwargs):


    _build_default(kwargs)
    es = Elasticsearch()

    # --- retrieve the document _ids
    from elasticsearch_dsl import Search
    s = Search(using=es, index=index, doc_type=doc_type)
    s = s.fields([])  # only get ids, otherwise `fields` takes a list of field names
    ids = [h.meta.id for h in s.scan()]

    n = s.count()

    # restrict the searchsize between 1 and 10
    searchsize = 10 if searchsize >= 10 else searchsize
    searchsize = 1 if searchsize < 1 else searchsize

    # restrict the cutv between > 0
    cutv = 0 if cutv<0 else cutv
    # store the sparse adjaency matrix



    I = []
    J = []
    V = []
    RV= []
    for i in ids:
        rv = es.mlt(index,doc_type,id=i, **kwargs)
        results = rv['hits']['hits']
        if len(results) > 0:
            for loop in xrange(searchsize):
                j = int(rv['hits']['hits'][loop]['_id'])
                score =  rv['hits']['hits'][loop]['_score']
                if score >= cutv:
                    I.append(ids.index(i))
                    J.append(j)
                    V.append(score)
                    RV.append(score)


    # construct the adjaency matrix using Sparse Index
    A = coo_matrix((V,(I,J)),shape=(n,n))
    RA = coo_matrix((RV,(I,J)),shape=(n,n))

    # construct a graph
    G = nx.from_scipy_sparse_matrix(A)

    # obtain the degree vlaues for all the nodes
    # {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 1, 8: 2, 9: 0,
    # 10: 4, 11: 0, 12: 4, 13: 1, 14: 1, 15: 1, 16: 4, 17: 4, 18: 3,
    # 19: 4, 20: 4, 21: 2, 22: 1, 23: 0, 24: 1, 25: 4, 26: 3, 27: 1,
    # 28: 1, 29: 2, 30: 3, 31: 4, 32: 1, 33: 4, 34: 2, 35: 2, 36: 1,
    # 37: 1, 38: 3, 39: 1, 40: 1, 41: 4, 42: 0, 43: 0, 44: 2, 45: 4,
    # 46: 1, 47: 1, 48: 2, 49: 0, 50: 1, 51: 1, 52: 3, 53: 1, 54: 2,
    # 55: 0, 56: 1, 57: 1, 58: 3, 59: 5, 60: 0, 61: 2, 62: 2, 63: 3,
    # 64: 5, 65: 1, 66: 1, 67: 4, 68: 5, 69: 2, 70: 4, 71: 3, 72: 4,
    # 73: 4, 74: 4, 75: 2, 76: 2, 77: 3, 78: 3, 79: 2, 80: 3, 81: 1,
    # 82: 1, 83: 2, 84: 0, 85: 2, 86: 4, 87: 2, 88: 1, 89: 1, 90: 4,
    # 91: 2, 92: 0, 93: 3, 94: 1, 95: 3, 96: 2, 97: 3, 98: 0, 99: 3,
    # 100: 0, 101: 1, 102: 1, 103: 2, 104: 3, 105: 4, 106: 4, 107: 1,
    # 108: 2, 109: 4, 110: 2, 111: 0, 112: 1, 113: 1, 114: 1, 115: 1,
    # 116: 4, 117: 4, 118: 3, 119: 4, 120: 4, 121: 2, 122: 1, 123: 0,
    # 124: 2, 125: 4, 126: 5, 127: 1, 128: 1, 129: 2, 130: 3, 131: 4,
    # 132: 1, 133: 4, 134: 2, 135: 2, 136: 0, 137: 1, 138: 3, 139: 0,
    # 140: 1, 141: 4, 142: 0, 143: 0, 144: 2, 145: 4, 146: 1, 147: 1,
    # 148: 2, 149: 0, 150: 1, 151: 1, 152: 3, 153: 1, 154: 2, 155: 0,
    # 156: 1, 157: 1, 158: 3, 159: 5, 160: 0, 161: 2, 162: 2, 163: 3,
    # 164: 5, 165: 1, 166: 1, 167: 4, 168: 5, 169: 2, 170: 4, 171: 3,
    # 172: 4, 173: 4, 174: 4, 175: 2, 176: 2, 177: 0, 178: 4, 179: 2,
    # 180: 3, 181: 1, 182: 1, 183: 2, 184: 0, 185: 2, 186: 4, 187: 2,
    # 188: 1, 189: 1, 190: 4, 191: 2, 192: 0, 193: 3, 194: 1, 195: 3,
    # 196: 2, 197: 3, 198: 0, 199: 3}

    D = G.degree().values()

    # partition the graph by modularity
    # return a dictionary
    #  {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 1, 8: 2, 9: 0, 10: 4, 11: 0, 12: 4, 13: 1, 14: 1, 15: 1, 16: 4, 17: 4, 18: 3, 19: 4,
    #  20: 4, 21: 2, 22: 1, 23: 0, 24: 1, 25: 4, 26: 3, 27: 1, 28: 1, 29: 2, 30: 3, 31: 4, 32: 1, 33: 4, 34: 2, 35: 2, 36: 1, 37: 1, 38:
    #  3, 39: 1, 40: 1, 41: 4, 42: 0, 43: 0, 44: 2, 45: 4, 46: 1, 47: 1, 48: 2, 49: 0, 50: 1, 51: 1, 52: 3, 53: 1, 54: 2, 55: 0, 56: 1,
    #  57: 1, 58: 3, 59: 5, 60: 0, 61: 2, 62: 2, 63: 3, 64: 5, 65: 1, 66: 1, 67: 4, 68: 5, 69: 2, 70: 4, 71: 3, 72: 4, 73: 4, 74: 4,
    #  75: 2, 76: 2, 77: 3, 78: 3, 79: 2, 80: 3, 81: 1, 82: 1, 83: 2, 84: 0, 85: 2, 86: 4, 87: 2, 88: 1, 89: 1, 90: 4, 91: 2, 92: 0,
    #  93: 3, 94: 1, 95: 3, 96: 2, 97: 3, 98: 0, 99: 3, 100: 0, 101: 1, 102: 1, 103: 2, 104: 3, 105: 4, 106: 4, 107: 1, 108: 2, 109: 4,
    #  110: 2, 111: 0, 112: 1, 113: 1, 114: 1, 115: 1, 116: 4, 117: 4, 118: 3, 119: 4, 120: 4, 121: 2, 122: 1, 123: 0, 124: 2, 125: 4,
    #  126: 5, 127: 1, 128: 1, 129: 2, 130: 3, 131: 4, 132: 1, 133: 4, 134: 2, 135: 2, 136: 0, 137: 1, 138: 3, 139: 0, 140: 1, 141: 4,
    #  142: 0, 143: 0, 144: 2, 145: 4, 146: 1, 147: 1, 148: 2, 149: 0, 150: 1, 151: 1, 152: 3, 153: 1, 154: 2, 155: 0, 156: 1, 157: 1,
    #  158: 3, 159: 5, 160: 0, 161: 2, 162: 2, 163: 3, 164: 5, 165: 1, 166: 1, 167: 4, 168: 5, 169: 2, 170: 4, 171: 3, 172: 4, 173: 4,
    #  174: 4, 175: 2, 176: 2, 177: 0, 178: 4, 179: 2, 180: 3, 181: 1, 182: 1, 183: 2, 184: 0, 185: 2, 186: 4, 187: 2, 188: 1, 189: 1,
    #  190: 4, 191: 2, 192: 0, 193: 3, 194: 1, 195: 3, 196: 2, 197: 3, 198: 0, 199: 3}
    # where key is the document id, and value is the parition id

    partition = community.best_partition(G)
    RAC = RA.tocsr()

    return get_map_document(partition, ids, D, RAC)

    #partition.values()

    # only for visualization purpose
    # pos = nx.spring_layout(G, k=0.05)
    #
    # colors =[]
    # import random
    # for randco in range(0,200):
    #     color = "#%06x" % random.randint(0, 0xFFFFFF)
    #     colors.append(color)
    # #colors = 'bgrcmykw'
    #
    # print 'Partition number ' + str(max(partition.values())+1)
    # for i, com in enumerate(set(partition.values())):
    #     list_nodes = [nodes for nodes in partition.keys()
    #                                 if partition[nodes] == com]
    #     nx.draw_networkx_nodes(G, pos, list_nodes, node_color=colors[i])
    # nx.draw_networkx_edges(G,pos)
    #
    # plt.show()


def get_map_document(partition, ids, degree, RAC):
    # according to the id partition assignment and degree information
    # notice degreee can be replaced by google rank, then need to be inversed cause degree larger is better, google rank smaller is better
    # a linear solution
    grouphub = {}
    docmap = {}

    for id,group in partition.iteritems():
        dg = degree[id]
        if group not in grouphub:
            grouphub[group] = ids[int(id)]  # if the partition is new, put the current document
        elif dg > grouphub[group]:
            grouphub[group] = ids[int(id)]  # if the new document in the same parition has larger degree, replace
        # if two document in the same partition have same degree, firstly visited one become hub

    # map the document id to hub document
    for id, group in partition.iteritems():
        if ids[int(id)] == grouphub[group]:
            v = 1
        else:
            v = RAC[id,ids.index(grouphub[group])]
        docmap[ids[int(id)]] = [grouphub[group],v]
    return docmap


 # Using documap to map a json document object to a representative document
 # The return value is exactly same as Shiyun's old method


def map_cluster_document(docmap, obj_json):
    obj_dict = json.loads(obj_json)
    mapped_doc_id = docmap.get(unicode(obj_dict['id']),[None,None])
    obj_dict["similar_to"] = mapped_doc_id[0]
    obj_dict["similarity_score"] = mapped_doc_id[1]
    return json.dumps(obj_dict)


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
