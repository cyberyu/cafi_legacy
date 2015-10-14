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
    Find the document most like the given artificial document (json); stop words can be passed in through the optional keyword argument stop_words=[word1, word2, ..]  
    Return: (id, score) if any match is found; otherwise, (-1, -Inf)
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
        return (int(results[0]['_id']),  results[0]['_score'])
    else:
        return (-1, -Inf)


def text_similarity_score_by_content(index, doc_type, mlt_fields, content, **kwargs):
    """
    Find the document whose mlt_fields are most like the given content.
    Content: unicode string
    mlt_fields: a list of fields to search for
    Return: (id, score) if any match is found; otherwise, (-1, -Inf)
    """

    _build_default(kwargs)
    es = Elasticsearch()
    body = {
        "query": {
        "more_like_this" : {
            "fields" : mlt_fields,
            "like_text": content, 
            "max_query_terms": kwargs["max_query_terms"],
            "min_term_freq": kwargs["min_term_freq"]
        }
      }}     
    rv = es.search(index=index, doc_type=doc_type, body=body)
    results = rv['hits']['hits']
    if len(results) > 0: 
        return (int(results[0]['_id']),  results[0]['_score'])
    else:
        return (-1, -Inf)

