__author__ = 'tanmoy'

# Code to check which API to use Alchemy or Apache Tika depending on the file type

#import TikaExtractCookie as TE #importing tika url based
import TikaExtractCookieDownloader as TE # downloading files before parsing with tika
import json
from alchemyapi import AlchemyAPI #importing alchemy api
import requests
import mechanize
import re
import cookielib
from checkBoilerpipe import HTMLExtractor
from TextClean import CleanText

#==============================
browser = mechanize.Browser()
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)
browser.set_handle_equiv(True)
#browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#browser.set_debug_http(True)
#browser.set_debug_redirects(True)
#browser.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#================================

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()
TIMEOUT = 30
class CheckLink :

    def __init__(self, url,extractor):
        self.url = url
        self.parsed_text = CleanText(self.check(url,extractor)).clean_text

    def get_headers(self,url): #Get the headers
        r = browser.open(url,timeout=TIMEOUT)
        return r.info()

    def check(self, url,extractor):
        r = self.get_headers(url)

        try:
            if "text/html" in r['Content-Type']: # checking if the response content-type is html
                #print "Parsed by Alchemy.. "
                """
                response1 = alchemyapi.text('url', url)
                #print json.dumps(response1,indent=1)
                if response1['status'] == 'OK':
                    return unicode(response1['text'].strip())
                else :
                    return ""
                """
                query1 = HTMLExtractor(url,extractor)
                return query1.parsed_text
            else:
                #print "Parsed by Tika.. "
                query1 = TE.DocumentConvertor(url) # using tika as a http service
                return unicode(query1.parsed_json['content'].strip())
        except Exception:
            query1 = TE.DocumentConvertor(url) # using tika as a http service
            return unicode(query1.parsed_json['content'].strip())

if __name__ == "__main__":
    url= raw_input("Enter url for check:")
    query1 = CheckLink(url,"DefaultExtractor")
    if query1.parsed_text == "":
        print "Its empty"
    else:
        print query1.parsed_text