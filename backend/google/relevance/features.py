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
        out = {"TDM": features, "terms": terms}
    
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
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = tokenize,    \
                             preprocessor = processor, \
                             stop_words = stopwords,   \
                             max_features = max_words, \
                             ngram_range= ngram) 

    # transforms our training data into feature vectors
    try:
        features = vectorizer.fit_transform(docs)
    except Exception:
        logging.error('Fail to vectorize the text data', exc_info=True)

    # the result to an array
    features = features.toarray()

    # tf-idf 
    if Tfidf:
        transformer = TfidfTransformer()
        try:
            features = transformer.fit_transform(features)
        except Exception:
            logging.error('Fail to convert to tf-idf', exc_info=True)
        features = features.toarray()

    return {'TDM': features, 'terms': vectorizer.get_feature_names()}
    
    
    
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
    
