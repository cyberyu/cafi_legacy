__author__ = 'tanmoy'

#!/usr/bin/env python2.7
import tika
from tika import parser
import ExcelToCsv as xc
import requests
import os
import sys
import mechanize
import cookielib
import download as dow

TIKA_SERVICE = 'http://localhost:1234/tika' #Have to change it to settings/local.py

target_path="./data/"   #Change target path to the folder where files will be stored

class DocumentConvertor:

    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def __init__(self,url):
        self.url = url
        self.parsed_json = self.document_to_text(url)
        target_path="./data/"



    def document_to_text(self,url):

        filepath = dow.download(url,target_path)

        if filepath[-4:] == ".doc" or filepath[-4:] == ".pdf" or filepath[-4:]=="ppt" or filepath[-5:] == "docx" or filepath[-5:]=="pptx":
            return self.tikaParser(filepath) # Might create new functions later is requirement arises
        elif filepath[-5:] == ".xlsx" :
            return self.tikaParser(filepath)
        elif filepath[-4:] == ".xls" :
            return self.tikaParserExcel(filepath) # Converts the file to .csv if it returns none from tika
        else:
            return "Unknown File Format"

    #using tika as service check readme for updates

    def tikaParser(self,path):
        parsed = parser.from_file(path,TIKA_SERVICE) # address of the local host created by tika jar
        return parsed

    def tikaParserExcel(self,path):
        parsed = parser.from_file(path,TIKA_SERVICE)
        #print unicode(parsed["content"]).strip()
        if parsed["content"] == None:  # need more general format

            xls_file = path
            csv_file = xc.csv_from_excel(xls_file,target_path)
            parsed1 = parser.from_file(csv_file,TIKA_SERVICE)
            return parsed1
        else:
            return parsed

    # simulate a browser to extract the text with cookie
    def tikaParserCookie(self, url):
        r = self.br.retrieve(url)
        query2 = parser.from_file(r[0],TIKA_SERVICE)
        os.remove(r[0])
        return query2

if __name__ == "__main__":
    #Testcases:
    #url= "http://www.shareholder.com/visitors/activeedgardoc.cfm?f=xls&companyid=AAPL&id=10916067"
    #url="/Users/tanmoy/Downloads/CAFI/APPLE_8-A12B.xls"  #Can accept both file path and url
    url_or_path = raw_input("Enter path or url to extract text content: ")
    query1 = DocumentConvertor(url_or_path)
    print unicode(query1.parsed_json['content'])
