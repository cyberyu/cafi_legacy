# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 14:16:44 2015

@author: kushi
"""

from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
import logging
from sklearn.preprocessing import binarize
from scipy.sparse import csr_matrix
import networkx as nx
import community


def distance_matrix(TDM, metric='cosine'):
    """
    calculate the distance matrix from data matrix

    @type  TDM:  and 2D numpy array  
    @param TDM:  term-document matrix, this can be either tf or tfidf, row corresponds to document, column corresponds to feature
    
    @type  metric:  a string object  
    @param metric:  a string can be 'cosine' (range between -1 and 1), 'correlation' ((range between 0 and 2))
    """   
    
    return pairwise_distances(TDM, Y=None, metric=metric)
    
    
def text_clustering(TDM, method='network', ncluster=None, distMetric='cosine', cutval = 0.5, maxnc = 50):
    """
    clustering the data

    @type  TDM:  and 2D numpy array  
    @param TDM:  term-document matrix, this can be either tf or tfidf, row corresponds to document, column corresponds to feature
    
    @type  method:  string object  
    @param method:  method of clustering
    
    @type  method:  integer object  
    @param method:  integer specify the number of clusters, if set to None, the algorithm will find the optimal number. only applies when clustering method = 'Kmeans'
    
    @type  distMetric:  string object  
    @param distMetric:  string to specify distance measure. e.g., 'cosine', 'correlation', only applies when method = 'network'
    
    @type  cutval:  float object  
    @param cutval:  floating value used to cut graph    
    
    @returns: a numpy array that contains the cluster ID corresponding to each sample
    """   
    
    if method == 'Kmeans':
        # find optimal number of clusters
        if ncluster is None:
            logging.info('started to find the optimal number of clusters')
            rg = np.arange(2, maxnc, 2)
            Si = []
            for nc in rg:
                km = KMeans(n_clusters=nc, init='k-means++', max_iter=100, n_init=1, verbose=True)
                km.fit(TDM)
                Si.append(metrics.silhouette_score(TDM, km.labels_, sample_size=1000))    
            # optimal number of cluster        
            ncOpt = rg[np.array(Si).argmax()]        
            logging.info('the optimal number of clusters found is %s', ncOpt)
        else:
            ncOpt = ncluster          
        
        # clustering
        logging.info('started to performan clustering')
        try:
            km = KMeans(n_clusters=ncOpt, init='k-means++', max_iter=100, n_init=1, verbose=True)
            km.fit(TDM)    
        except Exception:
            logging.error('failed to perform clustering', exc_info=True)
        logging.info('finish clustering')  
        
        clusterID = km.labels_
        
    elif method=='network':
        # use similarity to construct graph
        distMtx = 1-pairwise_distances(TDM, Y=None, metric=distMetric)
        mtxBinary = binarize(distMtx, threshold=cutval)
        #mtxBinary = bin(distMtx)
        G = nx.from_scipy_sparse_matrix(csr_matrix(mtxBinary)) 
        partition = community.best_partition(G)
        clusterID = partition.values()

    else:
        logging.error('undefined clustering method')
        
    return clusterID
    


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

    