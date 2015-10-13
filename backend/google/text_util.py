import numpy as np
from scipy.sparse import coo_matrix
from elasticsearch import Elasticsearch

def text_similarity_scores(index, doc_type, **kwargs):
    """
    return a sparse matrix whose (i,j) entry is the similarity score of document i and document j of /index_name/doc_type
    """

    #overwrite the ES default which seems not to work well for detecting duplication
    if not 'search_size' in kwargs:
        kwargs['search_size'] = 1 
    if not 'max_query_terms' in kwargs:
        kwargs['max_query_terms'] = 4000
    if not 'min_term_freq' in kwargs:
        kwargs['min_term_freq'] = 0

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

