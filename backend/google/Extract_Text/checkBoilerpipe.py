__author__ = 'tanmoy'


import io
import os
import sys
import json
from boilerpipe.extract import Extractor
from alchemyapi import AlchemyAPI #importing alchemy api
alchemyapi = AlchemyAPI()

"""
Boilerpipe:

    * DefaultExtractor
    * ArticleExtractor
    * ArticleSentencesExtractor
    * KeepEverythingExtractor
    * KeepEverythingWithMinKWordsExtractor # Not supported anymore
    * LargestContentExtractor
    * NumWordsRulesExtractor
    * CanolaExtractor

Alchemy API
    *Alchemy
"""

class HTMLExtractor :

    extractorFormat = ["DefaultExtractor", "ArticleExtractor", "ArticleSentencesExtractor", "KeepEverythingExtractor",
                          "LargestContentExtractor", "NumWordsRulesExtractor", "CanolaExtractor"]

    def __init__(self,url,extractortype):
        self.url = url
        self.extractortype = extractortype
        self.parsed_text = self.generate(url,extractortype)


    def generate(self, url, extractortype):
        try:
            if extractortype == 'Alchemy':
                response1 = alchemyapi.text('url', url)
                #print json.dumps(response1,indent=1)
                if response1['status'] == 'OK':
                    text = unicode(response1['text'].strip())
                else :
                    text =  ""

                return text
            elif extractortype in self.extractorFormat:
                extractor = Extractor(extractor=extractortype, url=url)
                extracted_text = extractor.getText()

                return extracted_text
            else :
                return "Extractor Type Not Supported"
        except Exception:
            return "Empty"


if __name__=='__main__': # Adding a few test cases
    """
    Boilerpipe:

        * DefaultExtractor
        * ArticleExtractor
        * ArticleSentencesExtractor
        * KeepEverythingExtractor
        * KeepEverythingWithMinKWordsExtractor
        * LargestContentExtractor
        * NumWordsRulesExtractor
        * CanolaExtractor

    Alchemy API
        *Alchemy
    """
    urlFormat = []
    urlFormat.append("https://www.endicottalliance.org/jobcutsreports.php") #recruiting page
    urlFormat.append("https://www.reddit.com/r/funny/")    #page of tabular data, list format
    urlFormat.append("http://www.ifeveryoneknew.com")      #page of quotations Simple page
    urlFormat.append("http://money.cnn.com/quote/quote.html?symb=IBM") #Stock Quote
    urlFormat.append("https://twitter.com/ibm") #twitter
    urlFormat.append("https://www.facebook.com/topic/Dhoom-4/106117332753865?source=whfrt&position=1&trqid=6205860601709811497") #Facebook
    urlFormat.append("http://www.nytimes.com") #Homepage of Nytimes
    urlFormat.append("http://www.nytimes.com/2015/10/16/world/asia/obama-troop-withdrawal-afghanistan.html") #Nytimes Article
    urlFormat.append("http://www.nytimes.com/2015/10/15/nytnow/latest-news-syria-european-union-lamar-odom.html")
    urlFormat.append("https://www.supplier-connection.net/SupplierConnection/about.html")
    urlFormat.append("http://www.wsj.com/articles/apple-suppliers-battle-for-control-of-taiwan-chip-company-1444821780") #Wallstreet article
    print urlFormat
    extractorType =[]
    extractorType.append("ArticleExtractor")
    extractorType.append("NumWordsRulesExtractor")
    extractorType.append("DefaultExtractor")
    extractorType.append("KeepEverythingExtractor")
    extractorType.append("Alchemy")
    #extractorType.append("KeepEverythingWithMinKWordsExtractor") #Extractor Type not supported
    print extractorType
    """
    for url in urlFormat:

        query = HTMLExtractor(url,extractorType)
        text = query.parsed_text
        print text
    """

    i = 1
    for extractor in extractorType :
        try:
            query = HTMLExtractor(urlFormat[10],extractor)
            text = query.parsed_text
            print text
            print "============================="
            filename = "./data/" + str(extractor)+str(i) + ".txt"
            foo = io.open(filename, "w+", encoding='utf-8')
            foo.write(unicode(text).strip())
            foo.close()
        except Exception:
            text = "HTTP Error"
            filename = "./data/" + str(extractor)+str(i) + ".txt"
            foo = io.open(filename, "w+", encoding='utf-8')
            foo.write(unicode(text).strip())
            foo.close()


        i = i + 1

        """
        foo = io.open("./data/" + "2.txt", "w+", encoding='utf-8')
        foo.write(unicode(text1).strip())
        foo.close()
        foo = io.open("./data/" + "3.txt", "w+", encoding='utf-8')
        foo.write(unicode(text2).strip())
        foo.close()
        """







