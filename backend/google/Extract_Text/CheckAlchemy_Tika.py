__author__ = 'tanmoy'

# Code to check which API to use Alchemy or Apache Tika depending on the file type

import TikaExtract as TE #importing tika url
import requests
import json
from alchemyapi import AlchemyAPI #importing alchemy api
import json


# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()

class checkLink :
    def __init__(self, url):
        self.url = url
        self.check(url)


    def check(self, url):
        r = requests.get(url)
        if "text/html" in r.headers["content-type"]: # checking if the response content-type is html
            response1 = alchemyapi.text('url', url)
            if response1['status'] == 'OK':
                print unicode(response1['text'])
        else:
            query1 = TE.DocumentConvertor(url) # using tika as a http service
            print unicode(query1.parsed_json['content'])

if __name__ == "__main__":
    url= raw_input("Enter url for check:")
    check = checkLink(url)