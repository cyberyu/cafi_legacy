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
from django.core import serializers

import logging
logger = logging.getLogger("CAFI")


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
        self.key = 'AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA' #Autocafi Developer Key
        self.client = googlemaps.Client(self.key)

    def simple_geocode(self,query):
        results = self.client.geocode(query)
        return results


# the search API key is now separated from AutoCafi account, and stay as a trial version
service = build("customsearch", "v1", developerKey="AIzaSyBeoj7no9n3EfELeBGujKdSdn1ydR5Jc00")
collection = service.cse()

@shared_task(default_retry_delay=3, max_retries=3)
def do_search(search, num_requests):
    # https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    search_engine_id = '012608441591405123751:clhx3wq8jxk'
    counter = 0
    start_page = search.last_stop
    logger.debug("Google Search: #request:"+ str(num_requests))
    # Make an HTTP request object
    for i1 in range(0, num_requests):
        if search.contain_result == 0:
            # This is the offset from the beginning to start getting the results from
            start_val = 1 + (start_page * 10)
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
                    logger.debug(obj)
                    obj.save()
                    do_download.delay(obj.id, obj.url)
                except Exception :
                    search.save()
                    logger.exception("Exception")

            counter =  len(response['items'])
            if counter < 10 : # Checks if the results returned are less than actual request of 10
                search.contain_result = 1 # Flag Set no more results
                start_page+=1
                search.last_stop = start_page
                search.save()
                break
            else:
                start_page+=1
                search.last_stop = start_page
                search.save()
        else:
            break

    search.save()
    return 1

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