# -*- coding: utf-8 -*-
"""
Created on Thu Dec 03 08:48:55 2015

@author: kushi
"""

import db
import features as ft
import active_learn as al
import numpy as np
import logging

        

class Classifier:

    def __init__(self, Tfidf=False, Nwords=5000, classifierMethod='SVM'):
        """
        initialize the class instance.

        @type  Tfidf:  boolean object
        @param Tfidf:  flag indicate if use Tfidf feature or TF feature

        @type  Nwords:  integer object
        @param Nwords:  an integer indicates the number of features to be extracted from text corpus
    
        @type classifierMethod: string object
        @param classifierMethod: classification method can be either 'LR','SVM' or 'SGB'
        """
             
        # feature extraction
        self.Tfidf = Tfidf
        self.Nwords = Nwords
        
        # classification
        self.classifierMethod = classifierMethod
        self.uncertaintyMethod = 'least confident'
        
        
    
    def readDB(self, dbconnection, textfield):
        """
        read data from database

        @type  dbconnection:  psycopg2 connection object
        @param dbconnection:  The established connection object to the Google Search Result database 
        
        @type textfield:  list object
        @param textfield: the list of Google Search Result table names to be concatenated as text field. Example: ['fulltext', 'srtitle']
        """        
        
        out = db.readDB(conn=dbconnection, textfield=textfield)
        self.docs = out["docs"]
        self.label = out["labels"]
        self.srids = out["srids"]
        


    # def load(self, filename):
    #     """
    #     load pick object from file
    #
    #     @type  filename:  string object
    #     @param filename:  file name
    #     """
    #
    #     logging.info('load training data feature vectorizer from: %s', filename)
    #     try:
    #         fileObj = open(filename, 'r')
    #         obj = pickle.load(fileObj)
    #     except Exception:
    #         logging.error('fail to read file and load pickle obj', exc_info=True)
    #     return obj



    # def save(self, saveFileName, saveType, memo):
    #     """
    #     save pickle object
    #
    #     @type  saveFileName:  string object
    #     @param saveFileName:  file name
    #
    #     @type  saveType:  string object
    #     @param saveType:  either 'featurefile' or 'classifile'
    #
    #     @type  memo:  string object
    #     @param memo:  description of the object saving
    #     """
    #
    #     fileObj = open(saveFileName, 'wb')
    #
    #     if (saveType == 'classifile'):
    #         pickle.dump(self.classifierObj, fileObj)
    #     elif (saveType == 'featurefile'):
    #         pickle.dump(self.featureObj, fileObj)
    #     else:
    #         logging.error('undefined saveType')
    #
    #     fileObj.close()
    #     logging.info('saved pickle obj to %s ', saveFileName)



    def buildFeature(self, oldData=None):
        """
        build the feature from the text corpus

        @type  oldData:  list object
        @param oldData:  the list of documents 
        """ 
	  
        if oldData==None:
		oldData = self.docs
        
        if (len(oldData)<5000):
            self.Nwords = 1000
        out = ft.build_features(oldData, keyWords=None, max_words=self.Nwords, Stem=True, Bigram=True, 
                                Tfidf=self.Tfidf, stopwords=True, Preprocess=True)
        # save model for feature extraction on new documents        
        self.featureObj = {'vectorizer': out['vectorizer'], 'tfMtx': out['tfMtx'], 'terms':out['terms']}
        # save the features
        self.features = out['TDM']



    def showFeatures(self, FTmatrix=None, terms=None):
        """
        build the feature from the text corpus

        @type  FTmatrix:  scipy.sparse.csr.csr_matrix
        @param FTmatrix:  tf or tfidf feature maxtrix, row corresponds to document, column corresponds to feature
        
        @type  terms:  list object
        @param terms:  the list of word features
        
        @returns: a list of tuple (terms_D, tf_D) sorted by descending order of term frequency. terms_D is a list of terms, tf_D is a list of term frequency 
        """ 

        if FTmatrix==None or terms==None: 
            FTmatrix = self.featureObj['tfMtx']
            terms = self.featureObj['terms']
            
        # sort feature by tf over all docs
        tf = FTmatrix.sum(axis = 0)
        tf = np.array(tf)[0].tolist()
        
        indDec = sorted(range(len(tf)), key=lambda k: tf[k], reverse=True)
        tf_D = [tf[i] for i in indDec]       
        terms_D = [terms[i] for i in indDec]
        
        return zip(terms_D, tf_D)        
    
     
    def prepareData(self):
        """
        prepare the data for the training & testing. set the training & testing id based on if the doc is labeled
        """ 
        
        # find train & test ID based on label or not
        #trainInd = [i for i, e in enumerate(self.label) if e != None]  # index of training data
        #testInd = [i for i, e in enumerate(self.label) if e == None]   # index of test data
        
        trainInd = [i for i, e in enumerate(self.label) if e != '']  # index of training data
        testInd = [i for i, e in enumerate(self.label) if e == '']   # index of test data

        logging.info('%s number of samples is used to train model, %s number of samples for testing', len(trainInd), len(testInd))
        logging.debug('train data indices are: ' + ','.join(map(str, trainInd)))
        logging.debug('test data indices are: ' + ','.join(map(str, testInd)))
 
        self.X_train = self.features[trainInd]
        self.X_test = self.features[testInd]
        self.y_train = [self.label[idx] for idx in trainInd]
    
        # document ID (database table key) without labeling
        self.id_test = [self.srids[idx] for idx in testInd]
        

    
    def train(self):
        """
        train a model
        """ 
        
        clf = al.train_classifier(self.X_train, self.y_train, method=self.classifierMethod)
        self.classifierObj = clf
               

    def recommend(self, predictOut, Nrecommendations): 
        """
        rank order the prediction score and make recommendation for labeling

        @type  predictOut:  Python dictionary object
        @param predictOut:  a Python dictionary {'relevanceScore':y_score, 'label':y, 'confidenceScore': distance}
        containing the predict results on test data. relevanceScore is a list of floating numbers. label is a list of predicted
        relevance flag. confidenceScore is a list of floating number, used to make recommendations
        
        @type  Nrecommendations:  integer
        @param Nrecommendations:  number of document to recommend for labeling
        
        @returns: a Python dictionary object {'ToConfirm_ID': ToConfirm_Id, 'ToConfirm_Score': ToConfirm_Score} 
        ToConfirm_ID is the document ID that require user to confirm. ToConfirm_Score is the predicted relevance score 
        correponding to the ToConfirm_ID          
        """ 
        
        # extract
        relevanceScore = predictOut['relevanceScore']
        confidenceScore = predictOut['confidenceScore']
        label = predictOut['label']        
        
         
        # sort the prediction results by confidenceScore for recommendation for labeling
        # samples with low confidence score are recommended for labeling  
        sortind = sorted(range(len(label)), key = lambda k: confidenceScore[k])
                 
        
        # recommendations
        ToConfirm_Id = [ self.id_test[i] for i in sortind[:Nrecommendations] ]
        ToConfirm_Score = [relevanceScore[i] for i in sortind[:Nrecommendations]]
        
        
        # all prediction records for database updata
        self.AllUpdate_Id = [ self.id_test[i] for i in range(len(label)) ]
        self.AllUpdate_Score = relevanceScore
        self.AllUpdate_Label = label
         
        return {'ToConfirm_ID': ToConfirm_Id, 'ToConfirm_Score': ToConfirm_Score} 
    
    
    
    def predict(self, X=None, classifierObj=None):
        """
        predict the relevance flag and relevance score for new or test data

        @type  X:  2D numpy array object 
        @param X:  contains the tf or tfidf. row corresponds to document, column corresponds to feature 
        
        @type  classifierObj:  sklearn classifier object
        @param classifierObj:  classifier object contains the trained model, and can be used for prediction
        
        @returns: a Python dictionary {'relevanceScore':y_score, 'label':y, 'confidenceScore': distance}
        containing the predict results on test data. relevanceScore is a list of floating numbers. label is a list of predicted
        relevance flag. confidenceScore is a list of floating number, used to make recommendations         
        """         
        
        if X is None:
            X = self.X_test
        if classifierObj is None:
            classifierObj = self.classifierObj
        out = al.calc_newdoc_relevance(X, classifier = classifierObj, method = self.uncertaintyMethod)
        return out

        
    def updateDB(self, dbconnection):
        """
        updated the predicted relevance score & relevance flag for the unlabeled data in search results

        @type  dbconnection:  psycopg2 connection object
        @param dbconnection:  The established connection object to the Google Search Result database         
        """                

        db.updateDB(dbconnection, value = self.AllUpdate_Score, idlist = self.AllUpdate_Id, type = 'relevanceScore', dbtable=db._DBTABLE_, dbfields=db._DBFIELDS_)
        db.updateDB(dbconnection, value = self.AllUpdate_Label, idlist = self.id_test, type = 'label', dbtable=db._DBTABLE_, dbfields=db._DBFIELDS_)



    def updateDBDuplication(self, dbconnection,docids, clusterids):
        db.updateDuplicationFlags(dbconnection,docids, clusterids)
            

    def projectNewData(self, newData, featureObj): 
        """
        project the new data to feature space already obtained from the existing text corpus

        @type  newData:  list object
        @param newData:  a list of new documents 
        
        @type  featureObj:  Python dictonary object
        @param featureObj:  A Python dictionary {'vectorizer': vectorizer, 'tfMtx': tfMtx, terms:terms}
        vectorizer is a sklearn object used to vectorize the text document. tfMtx is the term-frequency matrix corresponding 
        to existing text data. terms is list of words extracted from exising data
        
        @returns: an 2D numpy array represents the tf or tfidf matrix correponding to the new documents
        """        

        features = ft.build_features_for_newdoc(newData, featureObj, self.Tfidf)
        return features

 
   
    def showUnseenFeatures(self, newData):
        """
        show the new word features extracted from newData but not in the exising text corpus

        @type  newData:  list object
        @param newData:  a list of new documents 
        
        @returns: a list of tuple (terms_D, tf_D) sorted by descending order of term frequency. terms_D is a list of terms, tf_D is a list of term frequency 
        """ 
        
        # vectorize the new data: only extract TF feature
        out = ft.build_features(newData, keyWords=None, max_words=self.Nwords, Stem=True, Bigram=True, 
                                Tfidf=False, stopwords=True, Preprocess=True)        
        tfMtx = out['tfMtx']
        terms = out['terms'] 

        # find the terms in newData but not oldData
        oldTerms = self.featureObj['terms'] 
        
        
        # find index corresponding to new terms
        ind = [i for i in range(len(terms)) if terms[i] not in oldTerms]
        termsNew = [terms[i] for i in ind]
        tfMtxNew = tfMtx[:,ind]

        # return features ranked by TF over alls samples
        return self.showFeatures(tfMtxNew, termsNew)


     