# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 15:21:23 2015

@author: kushi
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer 
import string
from bs4 import BeautifulSoup  
import re
import logging
from scipy.sparse import vstack


def build_features_for_newdoc(doc, featureObj, ifTfidf):

    # laod object 
    tf_mdl = featureObj['vectorizer']
    tfMtxTrain = featureObj['tfMtx'] 
    
    # vectorize the new document
    logging.info('start to vectorize the new document')
    try:
        features = tf_mdl.transform(doc)
    except Exception:
        logging.error('Fail to vectorize the new text data', exc_info=True)
    
    if ifTfidf:
        tfidf_mdl = TfidfTransformer(norm = "l2", sublinear_tf=True, smooth_idf=True)
        try:
            tfidf_mdl = tfidf_mdl.fit(vstack([tfMtxTrain, features]))
            features = tfidf_mdl.transform(features)
        except Exception:
            logging.error('Fail to convert to tf-idf for the new doc', exc_info=True)
    
    # convert the result to an array
    features = features.toarray()        
    
    logging.info('finish vectorizing the new document')        
    
    return features

def build_features(docs, keyWords=None, max_words=5000, Stem=True, Bigram=True, Tfidf=True, stopwords=True, Preprocess=True):
    # build features: return features only consist of keyWords    

    logging.info('start to build bag-of-words predictors from text corpus')    
    logging.info('Predictors setup: Stem=%s, Bigram=%s, TFIDF=%s, Stopwords=%s, Preprocess=%s', Stem, Bigram, Tfidf, stopwords, Preprocess)
    
    # bag of words
    out = bag_of_words(docs, max_words=max_words, Stem=Stem, Bigram=Bigram, Tfidf=Tfidf, stopwords=stopwords, Preprocess=Preprocess)
    
    # extract columns corresponding to the keyWords
    if keyWords!=None:
        features = out['TDM']
        terms = out['terms']   
        colInd = [terms.index(key) for key in keyWords]
        features = features[:,colInd]
        terms = keyWords
        # only output features matching the keywords
        out['TDM'] = features
        out['terms'] = terms
    
    logging.info('finish building %s number of predictors', max_words)
    
    return out    



def bag_of_words(docs, max_words=5000, Stem=True, Bigram=True, Tfidf=True, stopwords=True, Preprocess=True):
    # build bag of words


    # tokenizer
    if Stem:
        tokenize = StemTokenizer
    else:
        tokenize = None

    if Preprocess:
        processor = preprocess
    else:
        processor = None

    # if use bi/tri-gram
    if Bigram:
        ngram = (1,3)
    else:
        ngram = (1,1)        
        
    # stop words: default
    if (stopwords==None) | (stopwords==False):
        stopwords = None
    if stopwords == True:
        stopwords = 'english'


    # Initialize the "CountVectorizer" object
    tf_mdl = CountVectorizer(analyzer = "word",   \
                             tokenizer = tokenize,    \
                             preprocessor = processor, \
                             stop_words = stopwords,   \
                             max_features = max_words, \
                             ngram_range= ngram) 

    # transforms our training data into feature vectors
    try:
        tf_mdl = tf_mdl.fit(docs)
        features = tf_mdl.transform(docs)
    except Exception:
        logging.error('Fail to vectorize the text data', exc_info=True)

    # save TF matrix
    tfMtx = features

    # tf-idf 
    if Tfidf:
        tfidf_mdl = TfidfTransformer(norm = "l2", sublinear_tf=True, smooth_idf=True)
        try:
            tfidf_mdl = tfidf_mdl.fit(features)
            features = tfidf_mdl.transform(features)
        except Exception:
            logging.error('Fail to convert to tf-idf', exc_info=True)
        
    # convert the result to an array
    features = features.toarray()

    return {'TDM': features, 'terms': tf_mdl.get_feature_names(), 'tfMtx': tfMtx, 'vectorizer': tf_mdl}
    
    
    
def StemTokenizer(text):
    
	#stemmer
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = word_tokenize(text)
    
    stemmer = PorterStemmer()
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))    
        
    # return a list: for a single doc    
    return stemmed
    

def preprocess(doc):
    
    # Removing HTML Markup
    text = BeautifulSoup(doc).get_text() 

    # Remove non-letters 
    letters_only = re.sub("[^a-zA-Z]", " ", text) 

    # Convert to lower case, split into individual words
    clean_doc = letters_only.lower()
     
    # return 
    return str(clean_doc)
    
