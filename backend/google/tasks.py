from __future__ import absolute_import
import traceback
from celery import shared_task
import random
import time
import json
from django.conf import settings
from django.core.cache import cache
cache.clear()
import googlemaps
from googleapiclient.discovery import build
from google.models import Search, SearchResult, GeoSearch
from google.helper import download
# from google.alchemyapi_python.alchemyapi import AlchemyAPI
# from google.Extract_Text.checkAlchemy_Tika import CheckLink


cache = settings.CACHE
def get_lock(key):
    while cache.get(key):
        time.sleep(0.2)
    return False

def set_lock(key):
    t = int(random.random()*100 + 100)
    print "wait a moment %s" % t
    cache.set(key, 1, px=t)

class GeocodingTest():
    def __init__(self):
        self.key = 'AIzaSyBeoj7no9n3EfELeBGujKdSdn1ydR5Jc00' #Autocafi Developer Key
        self.client = googlemaps.Client(self.key)

    def simple_geocode(self,query):
        results = self.client.geocode(query)
        return results
"""
def extract_text_AlchemyAPI_single(url_string):

    alchemyapi = AlchemyAPI()
    response1 = alchemyapi.text('url', url_string)
    if response1['status'] == 'OK':
        try:
            return unicode(response1['text'])
        except:
            pass
    else:
        return None
"""

service = build("customsearch", "v1", developerKey="AIzaSyBeoj7no9n3EfELeBGujKdSdn1ydR5Jc00")
collection = service.cse()

@shared_task(default_retry_delay=3, max_retries=3)
def do_search(search):
    #  https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    search_engine_id = '012608441591405123751:clhx3wq8jxk'
    num_requests = 3
    counter = 0
    counter1 = 0
    # Make an HTTP request object
    for i1 in range(0, num_requests):
        # This is the offset from the beginning to start getting the results from
        start_val = 1 + (i1 * 10)
        # Make an HTTP request object

        request = collection.list(q=search.string,
            num=10, #this is the maximum & default anyway
            start=start_val,
            cx=search_engine_id
        )
        response = request.execute()

        for i, doc in enumerate(response['items']):
            try:
                obj = SearchResult()
                obj.search = search
                obj.title = doc.get('title')
                obj.snippet = doc.get('snippet')
                obj.url = doc.get('link')
                obj.rank = start_val + i
                counter1 += 1
                obj.save()
                do_download.delay(obj.id, obj.url)
            except Exception :
                print "Exception"
                traceback.print_exc()

        counter =  len(response['items'])
        if counter < 10 :
            search.flag_check = 1
            search.save()
            break

    search.last_stop += (counter1/10) + 1
    search.save()

#@shared_task(default_retry_delay=3, max_retries=3)
def do_search_single(search, start_page):
    #  https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    print "holla"
    search_engine_id = '012608441591405123751:clhx3wq8jxk'
    obj_response =[]
    if search.flag_check == 0 :
        start_val = 1 + (start_page * 10)  # This is the offset from the beginning to start getting the results from
        counter = 0
        counter1 = 0
        # Make an HTTP request object

        request = collection.list(q=search.string,
            num=10, #this is the maximum & default anyway
            start=start_val,
            cx=search_engine_id
        )
        response = request.execute()
        for i, doc in enumerate(response['items']):
            try:
                obj = SearchResult()
                obj.search = search
                obj.title = doc.get('title')
                obj.snippet = doc.get('snippet')
                obj.url = doc.get('link')
                obj.rank = start_val + i
                counter1 += 1
                obj.save()
                #do_download.delay(obj.id, obj.url)
                print i + " : " +json.dumps(obj)
                obj_response.append(json.dumps(obj))
            except Exception:
                print "Exception"
                traceback.print_exc()

        counter =  len(response['items'])
        if counter < 10 :
            search.flag_check = 1
            search.save()

        search.last_stop = search.last_stop + (counter1/10)
        search.save()
        return json.dumps(obj_response)
    else:
        print json.dumps([])

#@shared_task(default_retry_delay=3, max_retries=3)
def do_demandsearch(search, start_page):
    #  https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    search_engine_id = '012608441591405123751:clhx3wq8jxk'
    start_val = 1 + (start_page * 10)  # This is the offset from the beginning to start getting the results from
    # Make an HTTP request object
    result = []
    request = collection.list(q=search.string,
        num=10, #this is the maximum & default anyway
        start=start_val,
        cx=search_engine_id
    )
    response = request.execute()
    obj_response =[]
    for i, doc in enumerate(response['items']):
        try:
            title = doc.get('title')
            snippet = doc.get('snippet')
            url = doc.get('link')
            rank = start_val + i
            obj_response.append({"title":title, "snippet":snippet, "url":url, "rank":rank})
        except Exception:
            print "Exception"
            traceback.print_exc()
    counter =  len(response['items'])
    if counter < 10 :
        search.flag_check = 1
        search.save()
    search.last_stop = search.last_stop + (counter/10)
    search.save()
    return json.dumps(obj_response)


@shared_task(default_retry_delay=3, max_retries=3)
def do_download(id, url):
    data = download(url)
    obj = SearchResult.objects.get(pk=id)
    obj.raw_file.name = data.get('path')
    obj.doc_type = data.get('doc_type')
    obj.text = data.get('text')
    obj.raw_html = data.get('raw_html')
    obj.save()


@shared_task(default_retry_delay=3, max_retries=3)
def do_geo_search(id, address):
    try:
        set_lock('geo_lock')
        query = GeocodingTest()
        if get_lock('geo_lock')==False:
            obj = GeoSearch.objects.get(pk=id)  # due to async, we want to get latest copy of geosearch object fresh to avoid conflict
            results = query.simple_geocode(address)
            if results:
                result = results[0]["geometry"]["location"]
                obj.lat = result.get('lat')
                obj.lng = result.get('lng')
                obj.status = 'good'
            else:
                obj.status = 'bad'
            obj.save()
    except Exception, exc:
        raise do_geo_search.retry(exc=exc)


if __name__ == '__main__':
    import os, sys
    PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend')
    sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from engagement.models import Project
    from google.models import Search, SearchResult
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

    project = Project(client="xx", name="bbbb")
    project.save()
    search = Search(project=project, string='olympic')
    search.save()
    do_search(search, 'olympics')