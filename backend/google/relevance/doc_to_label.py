# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 09:14:18 2015


@author: kushi
"""
#__package__="activeLearning"

from google.relevance import features
from google.relevance.features import build_features
import google.relevance.active_learn as AL
import psycopg2
from google.relevance import db
import sys
import numpy as np
import logging


IFDEBUG=1

def classify(conn, out, **kwargs):
    """
    Apply active learning classifier to predict relevance labels.

    @type  conn:  psycopg2 connection object
    @param conn:  The established connection object to the Google Search Result database

    @type  out:  Python dictionary object
    @param out:  A python dictionary {"docs": docs, "labels": label, "srids":srids} containing all the training and test data.  Docs are a list of text.  Labels are a list of relevance flags used for training.  srids is a list of document ids.

    @param kwargs:   remaining keyword arguments are passed to readDB functon, see below

    Args:
    @type textfield:  list object
    @param textfield: the list of Google Search Result table names to be concatenated as text field. Example: ['fulltext', 'srtitle']

    @type training_srids: list object
    @param training_srids: the list of document ids used as training data

    @type test_srids: list object
    @param test_srids: the list of document ids used as test data

    @returns:    Python data discionary object {"scores": ToConfirmScore, "srids":ToConfirm_Id}.  ToConfirmScore is the list of relevance scores that require user to confirm. Srids is the list of document ids that require user confimation.
    The predicted flag and relevance scores for all the test data will will be automatically updated in the table.
    """
    
    logging.info('start the recommendation process')



    # reading the input parameters
    Nwords = kwargs.pop('Nwords', 5000)
    Nrecommendations = kwargs.pop('Nrecommendations', 20)
    classificationMethod = kwargs.pop('classificationMethod', 'LR')


    docs = out["docs"]
    label = out["labels"]
    srids = out["srids"]

    logging.info('data label has %s number of "1",  %s number of "0" and %s number of NULL', sum(label=='1'), sum(label=='0'), sum(label==np.array(None)))


    # build features based on the text corpus
    if (len(docs)<5000):
        Nwords = 1000
    out = build_features(docs, keyWords=None, max_words=Nwords, Stem=True, Bigram=True, Tfidf=True, stopwords=True, Preprocess=True)
    features = out['TDM']
    #terms = out['terms']

    # based on whether the label is NULL or Not NULL,  to split training and test data

    #trainInd = [i for i, e in enumerate(label) if (e != None and len(e)!=0)]  # index of training data
    trainInd = [i for i, e in enumerate(label) if (e==db._RELEVANCE_LABEL_NEG_ or e==db._RELEVANCE_LABEL_POS_ )]  # index of training data

    testInd = [i for i, e in enumerate(label) if (e!=db._RELEVANCE_LABEL_NEG_ and e!= db._RELEVANCE_LABEL_POS_) ]   # index of test data

    logging.info('%s number of samples is used to train model, %s number of samples for testing', len(trainInd), len(testInd))
    logging.debug('train data indices are: ' + ','.join(map(str, trainInd)))
    logging.debug('test data indices are: ' + ','.join(map(str, testInd)))

#    Nsamp = len(label)
#    trainInd = [i for i,j in enumerate(label) if j!=None]
#    testInd = list(set(range(Nsamp))-set(trainInd))

    X_train = features[trainInd]
    X_test = features[testInd]
    #y_train = label[trainInd]
    y_train = [label[idx] for idx in trainInd]



    # document ID
    id_test = [srids[idx] for idx in testInd]

    # use active learning to recommend more docs for labeling

    prediction = AL.process(X_train, y_train, X_test, Nrecs=Nrecommendations, method=classificationMethod, rankMethod='least confident')
    IDtoLabel = prediction['recommendation']  # all the

    ToConfirm_Id = [id_test[idx] for idx in IDtoLabel.keys()]
    ToConfirmScore = IDtoLabel.values()

    logging.info('recommend %s documents for labeling', Nrecommendations)
    logging.debug('id and relevance scores of recommended documents for labeling are: ' + ','.join(map(str, zip(ToConfirm_Id, ToConfirmScore))))


    # predicted label
    classifier = prediction['classifier']
    y_test_predicted = classifier.predict(X_test)


    # relevance score for all the test data
    AllIDScores = prediction['rawscore']

    #AllUpdate_Id = [srids[idx] for idx in AllIDScores.keys()]
    AllUpdate_Id = [id_test[idx] for idx in AllIDScores.keys()]
    AllUpdate_Score = AllIDScores.values()

    # update label & rank (overwrite the old ones)
    logging.info('start to save the recommendation results to database')



    # update prediction label
    #db.updateDB(conn, value = y_test_predicted, idlist = id_test, type = 'label', dbtable=db._DBTABLE_, dbfields=db._DBFIELDS_)
    db.updateDB(conn, value = AllUpdate_Score, idlist = AllUpdate_Id, type = 'relevanceScore', dbtable=db._DBTABLE_, dbfields=db._DBFIELDS_)
    db.updateDB(conn, value = y_test_predicted, idlist = id_test, type = 'label', dbtable=db._DBTABLE_, dbfields=db._DBFIELDS_)

    print 'AllUpdate_Id'
    print str(len(AllUpdate_Id))
    print AllUpdate_Id
    # update relevanceScore
    #db.updateDB(conn, value = ToConfirmScore, idlist = ToConfirm_Id, type = 'relevanceScore', dbtable=db._DBTABLE_, dbfields=db._DBFIELDS_)
    # close connection to database
    conn.close()

    logging.info('finish saving the recommendation results to database')
    logging.info('finish the recommendation process')

    return({"scores": ToConfirmScore, "srids":ToConfirm_Id})


def debug():
    print 'Start Debugging'

def main(arg=None):
    """
    The main example code of how to invoke active learning procedure
    """

    #establish connection
    conn_string = "host='localhost' dbname='cafi' user='cafi' password='awesome'"
    conn = psycopg2.connect(conn_string)

    #Define data columns
    tf=["text", "title", "snippet"]

    #Retrieve data
    text_file = db.readDB(conn, textfield = tf)

    #Apply Classifier and Obtain Ids to be confirmed
    ids_to_confrim = classify(conn, text_file, textfield = tf)

    #print out recommended doc ids and scores


    print ids_to_confrim['srids']

    print ids_to_confrim['scores']


if __name__== "__main__":
    sys.exit(main())

