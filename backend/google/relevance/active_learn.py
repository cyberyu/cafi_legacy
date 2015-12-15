# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 17:23:24 2015

active learning functions

@author: kushi
"""

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from collections import OrderedDict
import random
import itertools
import logging


def process(X_train, y_train, X_test, Nrecs=None, method='SVM', rankMethod='least confident'):
    # 1. train classifier
    classifier = train_classifier(X_train, y_train, method)

    # 2. make recommendation for labeling: return test data ID for labeling
    if Nrecs==None:
        Nrecs = X_test.shape[0]

    all_pairs = rank_candidate(X_test, classifier, Nrecs=X_test.shape[0], rankMethod=rankMethod)
    top_pairs = dict((key, value) for (key, value) in itertools.islice(all_pairs.iteritems(), Nrecs))
    
    return{'recommendation': top_pairs, 'rawscore': all_pairs, 'classifier': classifier}

def train_classifier(X, y, method='SVM'):

    if method=='SVM':        
        classifier = SVC(kernel='linear', probability=True)        
    elif method== 'SGB':
        classifier = GradientBoostingClassifier(n_estimators=200, max_depth=3)
    else:
        #classifier = LogisticRegression(penalty='l2', multi_class='ovr')
        classifier = LogisticRegression(penalty='l2')


    logging.info('starting traing a model with method of %s', method)
    logging.info('training label has %s number of "1" and %s number of "0"', y.count(1), y.count(0))

    # train classifier     
    random.seed(123)
    try:
        classifier = classifier.fit(X,y)
    except Exception:
        logging.error('Failed to train the model', exc_info=True)
    
    logging.info('finish training the model')   
    
    return classifier
    



def calc_newdoc_relevance(X, classifier, method = 'least confident'):
    # caluclate the relevance score for a new document
    # X is the feature vector corresponding to the document    
    
    # calculate relevance score
    logging.info('start to calculate relevance score for a new doc') 
    
    # prediction confidence score
    y_score = classifier.predict_proba(X)       
    if(method=='least confident'):
	      distance = np.amax(y_score, axis=1)
    elif(method=='margin'):	   
		 y_score[:,::-1].sort(axis=1)
		 distance = y_score[:,0]-y_score[:,1]
    elif(method=='entropy'):
		 distance = np.apply_along_axis(lambda x: np.dot(x, np.log(x)), 1, y_score)
    else:
		logging.error('undefined uncertainty ranking method to rank relevance score')
    logging.info('finish calculating relevance score for a new doc')
    
    
    # predict label    
    logging.info('start to predict class label for a new doc')
    try:
        y = classifier.predict(X)
    except Exception:
        logging.error('failed to predict class label for a new doc')
    logging.info('finish predicting class label for a new doc')
    
    return {'relevanceScore':y_score[:,1], 'label':y, 'confidenceScore': distance}



def rank_candidate(X, classifier, Nrecs=None, rankMethod='least confident'):
    # rank the test data sample and make recommendations

    logging.info('start calculating relevance score') 

    # prediction confidence score
    y_score = classifier.predict_proba(X)  
    # calculate certainty/distance: the 3 method will be equivalent for 2 classes case     
    if(rankMethod=='least confident'):
        distance = np.amax(y_score, axis=1)
    elif(rankMethod=='margin'):	   
        y_score[:,::-1].sort(axis=1)
        distance = y_score[:,0]-y_score[:,1]
    elif(rankMethod=='entropy'):
        distance = np.apply_along_axis(lambda x: np.dot(x, np.log(x)), 1, y_score)
    else:
        logging.error('undefined uncertainty ranking method to rank relevance score')

    logging.info('finish calculating relevance score') 
    logging.info('start to rank the relevance score')
    
    # number of samples
    Nsamp = len(distance)
    pairs = dict(zip(range(Nsamp), distance))
    t2 = sorted(pairs.items(), key=lambda k: k[1])
    t3 = OrderedDict(t2)
    sorted_pairs = OrderedDict(zip(t3.keys(), [round(v, ndigits=3) for v in t3.values()]))    
       
    # make recommendations: the index of the sample to be recommended for labeling
    if Nrecs==None:
        Nrecs = Nsamp
    if Nrecs>Nsamp:
        logging.warning('There are only %s samples left that can be labeled', repr(Nrecs))
        Nrecs = Nsamp

    # subset of OrderedDict    
    top_pairs = OrderedDict(sorted_pairs.items()[:Nrecs])
    
    logging.info('finish ranking the relevance score')    
    
    return top_pairs



def add_answers(X_train, X_test, y_train, y_newlabel, IDrec):
    
    # after get expert label the new evidence    
    # add answer: add new evidence to training data
    
    # features
    X_train_new = np.concatenate((X_train, X_test[IDrec,]))
    mask = np.ones(X_test.shape[0], dtype=bool) # all elements included/True.
    mask[IDrec] = False 
    X_test_new = X_test[mask, ]

    # labels
    y_train_new = np.concatenate((y_train, y_newlabel))

    return {'X_train': X_train_new, 'X_test': X_test_new, 'y_train': y_train_new}



