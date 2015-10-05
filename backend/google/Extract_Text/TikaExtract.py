__author__ = 'tanmoy'

#!/usr/bin/env python2.7
import tika
from tika import parser
import ExcelToCsv as xc
import requests
import os
import sys

class DocumentConvertor :
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
        parsed = parser.from_file(url,'http://localhost:1234/tika') # address of the local host created by tika jar
        return parsed

    def tikaParserExcel(self,url):
        parsed = parser.from_file(url)

        if parsed["content"] == None:
            # Open the url provided as an argument to the function and read the content
            if str(url).startswith('http://') or str(url).startswith('https://'):
                base = "./data/"
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

            csv_file = xc.csv_from_excel(xls_file)
            parsed1 = parser.from_file(csv_file,'http://localhost:1234/tika')
            os.remove(csv_file)
            os.remove(xls_file)
            return parsed1
        else:
            return parsed

if __name__ == "__main__":
    #Testcases:
    #url= "http://www.shareholder.com/visitors/activeedgardoc.cfm?f=xls&companyid=AAPL&id=10916067"
    #url="/Users/tanmoy/Downloads/CAFI/APPLE_8-A12B.xls"  #Can accept both file path and url
    url_or_path = raw_input("Enter path or url to extract text content: ")
    query1 = DocumentConvertor(url_or_path)
    print unicode(query1.parsed_json['content'])

