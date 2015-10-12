__author__ = 'tanmoy'

import os
import sys
import re
import string
import itertools
import unicodedata
import nltk
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures,TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import EnglishStemmer
import gensim
from gensim.parsing.preprocessing import STOPWORDS

from checkAlchemy_Tika import CheckLink #Refer to the code Input Url and Output Noisy Text

"""
Some functions are written for later review cases. 
"""

class CleanText:
    def __init__(self, text):
        self.text = text
        self.clean_text = self.process_text(self.text)

    def lower(self,text):
        """change everything to lowercase
        """
        text = text.lower()
        return text


    def remove_extra_space(self, text):
        """Remove multiple whitespaces and multiple newline with one of each
        """
        #text = " ".join(text.split())
        exp = re.compile("[^\S\r\n]")  # Remove multiple spaces except newlines
        exp.sub("",text)
        text =  re.sub('\n+','\n',text)
        text = re.sub(r'(\W)(?=\1)', '', text)
        return text

    def remove_special_chars(self, text):
        """remove all special characters except the period (.)
           comma (,) and question mark (?)
           for instance, ">", "~", ", $, |, etc.
        """
        schars = ''.join([a for a in string.punctuation if a not in ".,?"])

        text = re.sub('[%s]' % re.escape(schars), '', text)
        text = re.sub(r'&#x([a-fA-F\d]+);',lambda m: unichr(int(m.group(1),base=16)),text)
        return text

    def split_words(self, text, stopwords =STOPWORDS):
        """Break text into a list of single words. Ignore any token that falls into the 'stopwords' set
        """
        return [word
                for word in gensim.utils.tokenize(text, lower=True)
                if word not in STOPWORDS and len(word)>3]

    def split_wordsBasic(self, text, stopwords =STOPWORDS):
        """Break text into a list of single words. Ignore any token that falls into the 'stopwords' set
        """
        x = [word.strip()
                for word in text.split(' ')
                if word.lower() not in STOPWORDS]
        print x
        return x

    def remove_punctuation(self, text):
        """Replace punctuation mark with space
        """
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        return text

    def split_sentences(self, text):
        """Returns split sentences list and index of splitting point
           Reference:
           http://stackoverflow.com/questions/8465335/a-regex-for-extracting-
                  sentence-from-a-paragraph-in-python
        """
        sentenceEnders = re.compile(r"""
            # Split sentences on whitespace between them.
            (?:               # Group for two positive lookbehinds.
              (?<=[.!?])      # Either an end of sentence punct,
            | (?<=[.!?]['"])  # or end of sentence punct and quote.
            )                 # End group of two positive lookbehinds.
            (?<!  Mr\.   )    # Don't end sentence on "Mr."
            (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
            (?<!  Jr\.   )    # Don't end sentence on "Jr."
            (?<!  Dr\.   )    # Don't end sentence on "Dr."
            (?<!  Prof\. )    # Don't end sentence on "Prof."
            (?<!  Sr\.   )    # Don't end sentence on "Sr."
            (?<!  Sen\.  )
            (?<!  Ms\.   )
            (?<!  Rep\.  )
            (?<!  Gov\.  )
            \s+               # Split on whitespace between sentences.
            """, re.IGNORECASE | re.VERBOSE)
        sentenceList = sentenceEnders.split(text)
        st_index = [0]
        for s in sentenceEnders.finditer(text):
            st_index.append(s.start())
        return sentenceList, st_index

    def process_text(self, text):
        """
        Preprocess a string and returning the result as a unicode string
        :param text
        :return: text
        """
        text =  text.encode("ascii","ignore").strip()
        text = self.remove_extra_space(text)
        text = self.remove_special_chars(text)

        sentenceList = text.split('\n')
        sentenceList = [sentence.strip() for sentence in sentenceList
                        if len(set(sentence))>4]
        text = '\n'.join(sentenceList)
        text = re.sub('\n+','\n',text)
        return text



if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    #url ="http://idebate.org/sites/live/files/CV-Template_DPM.pdf"
    #url = "http://stackoverflow.com/questions/15418561/convert-a-word-to-a-list-of-chars"
    text = CheckLink(url).parsed_text
    clean_Text = CleanText(text).clean_text
    print clean_Text