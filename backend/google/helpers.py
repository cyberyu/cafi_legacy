
from googleapiclient.discovery import build
#import redis
#import json
#import time
#import requests
import urllib
from bs4 import BeautifulSoup
#from alchemyapi import AlchemyAPI
from google.models import Search, SearchResult


def extract_html_single(url_string):
    html = urllib.urlopen(url_string).read()
    return html


#print extract_html_single('https://en.wikipedia.org/wiki/Layoff')

def extract_text_single(html_string):
    soup = BeautifulSoup(html_string)
    for script in soup(["script","style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

#
# def extract_text_AlchenyAPI_single(url_string):
#     alchemyapi = AlchemyAPI()
#     response1 = alchemyapi.text('url', url_string)
#     if response1['status'] == 'OK':
#         try:
#             #print (unicode(response1['text']))
#             return unicode(response1['text'])
#         except:
#
#             pass
#
#     else:
#         return None
#
#

if __name__ == '__main__':
    import os, sys
    PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend')
    sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")



service = build("customsearch", "v1", developerKey="AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA")
collection = service.cse()

def do_search(search, string):
    #  https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    search_engine_id = '012608441591405123751:clhx3wq8jxk'

    start_val = 0
    request = collection.list(
        q=string,
        # num=10, #this is the maximum & default anyway
        # start=start_val,
        cx=search_engine_id
    )
    response = request.execute()

    for i, doc in enumerate(response['items']):
        obj = SearchResult()
        obj.search = search
        obj.title = doc.get('title')
        obj.snippet = doc.get('snippet')
        obj.url = doc.get('link')
        obj.rank = start_val + i
        obj.text = extract_text_single(extract_html_single(obj.url))
        #obj.text = extract_text_AlchenyAPI_single(obj.rul)
        obj.save()


if __name__ == '__main__':
    from engagement.models import Project
    from google.models import Search, SearchResult
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

    project = Project(client="xx", name="bbbb")
    project.save()
    search = Search(project=project, string='olympic')
    search.save()
    do_search(search, 'olympics')

