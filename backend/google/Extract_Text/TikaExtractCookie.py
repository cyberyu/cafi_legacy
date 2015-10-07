__author__ = 'tanmoy'
__author__ = 'shiyu'

#!/usr/bin/env python2.7
import tika
from tika import parser
import ExcelToCsv as xc
import requests
import os
import sys
import mechanize
import cookielib


TIKA_SERVICE = 'http://localhost:1234/tika'
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



    def document_to_text(self,url):

        if url[-4:] == ".doc" or "f=doc" in url:
            return self.tikaParser(url) # Might create new functions later is requirement arises
        elif url[-4:] == ".pdf" or "f=pdf" in url:
            return self.tikaParser(url)
        elif url[-4:] == ".ppt" or "f=ppt" in url:
            return self.tikaParser(url)
        elif url[-5:] == ".docx" or "f=docx" in url:
            return self.tikaParser(url)
        elif url[-5:] == ".pptx" or "f=pptx" in url:
            return self.tikaParser(url)
        elif url[-4:] == ".xls" or "f=xls" in url:
            return self.tikaParserExcel(url) # Converts the file to .csv if it returns none from tika
        elif url[-5:] == ".xlsx" or "f=xlsx" in url:
            return self.tikaParserExcel(url) # Converts the file to .csv if it returns none from tika
        elif url[-4:] == ".csv" or "f=csv" in url:
            return self.tikaParser(url)
        else:
            return "Unknown File Format"

    #using tika as service check readme for updates

    def tikaParser(self,url):
        parsed = parser.from_file(url,TIKA_SERVICE) # address of the local host created by tika jar
        return parsed

    def tikaParserExcel(self,url):
        parsed = parser.from_file(url, TIKA_SERVICE)
        #print unicode(parsed["content"]).strip()
        if parsed["content"] == None:  # need more general format
            # Open the url provided as an argument to the function and read the content
            if str(url).startswith('http://') or str(url).startswith('https://'):
                base = target_path
                f = requests.get(url, stream=True)
                file_path= os.path.basename(url)
                xls_file = base + ''.join([file_path.split('.')[0],'.xls'])
                if f.status_code == 200:
                    with open(xls_file, 'wb') as r:
                        for chunk in f.iter_content():
                            r.write(chunk)
                    r.close()
            else:
                xls_file = url

            csv_file = xc.csv_from_excel(xls_file,target_path)
            parsed1 = parser.from_file(csv_file,TIKA_SERVICE)
            #os.remove(csv_file)
            #os.remove(xls_file)
            return parsed1
        elif unicode(parsed["content"]).strip().startswith("Access denied"):
            return self.tikaParserCookie(url)

        else:
            return parsed

    # simulate a browser to extract the text with cookie
    def tikaParserCookie(self, url):
        r = self.br.retrieve(url)
        query2 = parser.from_file(r[0],TIKA_SERVICE)
        os.remove(r[0])
        return query2

