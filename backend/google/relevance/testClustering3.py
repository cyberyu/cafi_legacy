# -*- coding: utf-8 -*-
"""
Created on Tue Dec 08 14:07:28 2015

@author: kushi
"""

import psycopg2
from classifierAPI import Classifier
from clustering import text_clustering

# data base connection
conn_string = "host='localhost' dbname='cafi' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)

# text string to read data
tf=["text", "title", "snippet"]

# initial class
myClf = Classifier(Tfidf=True, Nwords=1000)

# read data from data base
myClf.readDB(conn, tf)

# build tfidf matrix
myClf.buildFeature()
Xtfidf = myClf.features
srids = myClf.srids

# clustering: compare the network vs Kmeans method
clusterID1 = text_clustering(Xtfidf, method='network', distMetric='cosine', cutval=0.9)
print("number of clusters is %s", len(set(clusterID1)))
print clusterID1
#clusterID2 = text_clustering(Xtfidf, method='Kmeans', ncluster=None, maxnc=50)
#print("number of clusters is %s", len(set(clusterID2)))


print ('srids')
print srids

# order the doc for visualization purpose

#
# docs = myClf.docs
# ind1 = sorted(range(len(docs)), key=lambda k: clusterID1[k])
# sortID1 = [clusterID1[i] for i in ind1]
#
# print sortID1
#
# sortDoc1 = [docs[i] for i in ind1]
#
# print sortDoc1
#ind2 = sorted(range(len(docs)), key=lambda k: clusterID2[k])
#sortID2 = [clusterID2[i] for i in ind2]
#sortDoc2 = [docs[i] for i in ind2]
