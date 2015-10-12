__author__ = 'tanmoy'

import os
import io
import re
import string
#import nltk
#import gensim
#from gensim.parsing.preprocessing import STOPWORDS
from TikaExtractCookie import DocumentConvertor

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
        exp = re.compile("[^\S\r\n]")  # Remove multiple spaces except newlines
        exp.sub("",text)
        text =  re.sub('\n+','\n',text) # Remove multiple newlines
        text = re.sub(r'(\W)(?=\1)', '', text) # Replace many repetitive character with same character
        text = re.sub(r"(?<=[a-z])\r?\n"," ", text)  #positive lookbehind assertion
        return text

    def remove_special_chars(self, text):
        """remove all special characters except the period (.)
           comma (,) and question mark (?)
           for instance, ">", "~", ", $, |, etc.
        """
        schars = ''.join([a for a in string.punctuation if a not in ".,?$\"\'></"])

        text = re.sub('[%s]' % re.escape(schars), '', text)
        text = re.sub(r'&#x([a-fA-F\d]+);',lambda m: unichr(int(m.group(1),base=16)),text)
        return text

    '''
    def split_words(self, text, stopwords =STOPWORDS): #kept for tokenizing later
        """Break text into a list of single words. Ignore any token that falls into the 'stopwords' set
        """
        return [word
                for word in gensim.utils.tokenize(text, lower=True)
                if word not in STOPWORDS and len(word)>3]
    '''

    def remove_punctuation(self, text): #To remove punctions though was not needed
        """Replace punctuation mark with space
        """
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        return text


    def process_text(self, text): # main function, calls the rest
        """
        Preprocess a string and returning the result as a unicode string
        :param text
        :return: text
        """
        text = unicode(text)
        print text
        text =  text.encode("ascii","ignore").strip()
        text = self.remove_extra_space(text)
        text = self.remove_special_chars(text)

        sentenceList = text.split('\n')
        sentenceList = [sentence.strip() for sentence in sentenceList
                        if len(set(sentence))>4]
        text = '\n'.join(sentenceList)
        text = re.sub('\n+','\n',text)
        return unicode(text)



if __name__ == "__main__": # For testcases

    url = "http://www.nytimes.com/2015/10/13/business/for-profit-colleges-accused-of-fraud-still-receive-us-funds.html?hp&action=click&pgtype=Homepage&module=first-column-region&region=top-news&WT.nav=top-news"
    #url ="https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html"
    #url ="http://www.shareholder.com/visitors/activeedgardoc.cfm?f=xls&companyid=AAPL&id=10916067"
    text = CheckLink(url).parsed_text
    #text = DocumentConvertor("Path").parsed_json['content']
    clean_Text = CleanText(text).clean_text
    """
    Check Writing to a file
    foo = io.open("./data/" + "1.txt", "w+", encoding='utf-8')
    foo.write(unicode(clean_Text))
    foo.close()
    """
    print clean_Text