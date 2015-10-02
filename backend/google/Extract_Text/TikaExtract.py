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
        self.parsed_text = self.document_to_text(url)

    def document_to_text(self,url):

        if url[-4:] == ".doc" or "f=doc" in url:
            return self.tikaParser(url)
        elif url[-4:] == ".pdf" or "f=pdf" in url:
            return self.tikaParser(url)
        elif url[-4:] == ".ppt" or "f=ppt" in url:
            return self.tikaParser(url)
        elif url[-5:] == ".docx" or "f=docx" in url:
            return self.tikaParser(url)
        elif url[-5:] == ".pptx" or "f=pptx" in url:
            return self.tikaParser(url)
        elif url[-4:] == ".xls" or "f=xls" in url:
            return self.tikaParser(url)
        elif url[-5:] == ".xlsx" or "f=xlsx" in url:
            return self.tikaParser(url)
        elif url[-4:] == ".csv" or "f=csv" in url:
            return self.tikaParser(url)
        else:
            return "Unknown File Format"


    def tikaParser(self,url):
        parsed = parser.from_file(url)

        if parsed["content"] == None:
            # Open the url provided as an argument to the function and read the content
            if str(url).startswith('http://') or str(url).startswith('https://'):

                f = requests.get(url, stream=True)
                file_path= os.path.basename(url)
                xls_file = ''.join([file_path.split('.')[0],'.xls'])
                if f.status_code == 200:
                    with open(xls_file, 'wb') as r:
                        for chunk in f.iter_content():
                            r.write(chunk)
                    r.close()
            else:
                xls_file = url

            csv_file = xc.csv_from_excel(xls_file)
            parsed1 = parser.from_file(csv_file)
            os.remove(csv_file)
            os.remove(xls_file)
            return parsed1["content"]
        else:
            return parsed["content"]

if __name__ == "__main__":
    #Options:
    #url= "http://www.shareholder.com/visitors/activeedgardoc.cfm?f=xls&companyid=AAPL&id=10916067"
    #url="/Users/tanmoy/Downloads/CAFI/APPLE_8-A12B.xls"  #Can accept both file path and url
    url_or_path = raw_input("Enter path or url to extract text content: ")
    query1 = DocumentConvertor(url_or_path)
    print query1.parsed_text

