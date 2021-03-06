from __future__ import absolute_import
import traceback
from celery import shared_task
import random
import time
import json
from swampdragon.pubsub_providers.data_publisher import publish_data
from django.conf import settings
import googlemaps
from googleapiclient.discovery import build
from google.models import Search, SearchResult, GeoSearch
from google.helper import download
from google.relevance import classifierAPI, clustering
import psycopg2
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


def publish_search_status(search_result):
    status = {}
    searches = cache.keys('search.*')
    for key in searches:
        sid = int(key.split('.')[-1])
        value = cache.hgetall(key)
        status[sid] = {}
        status[sid]['to_process'] = value.get('to_process', 0)
        status[sid]['processed'] = value.get('processed', 0)
        if (status[sid]['to_process'] == status[sid]['processed']
            and status[sid]['to_process'] and status[sid]['processed']):
            s = Search.objects.get(pk=sid)
            s = Search.objects.get(pk=sid)
            s.status = 2  # mark status as done
            s.save()
            cache.delete(key)
    channel = 'project_%s_search' % search_result.search.project.id
    print channel, status
    publish_data(channel, status)
    return status


class GeocodingTest():
    def __init__(self):
        self.key = 'AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA' #Autocafi Developer Key
        self.client = googlemaps.Client(self.key)

    def simple_geocode(self, query):
        results = self.client.geocode(query)
        return results


@shared_task(default_retry_delay=3, max_retries=3)
def do_search(search, num_requests):
    # the search API key is now separated from AutoCafi account, and stay as a trial version
    service = build("customsearch", "v1", developerKey="AIzaSyBeoj7no9n3EfELeBGujKdSdn1ydR5Jc00")
    collection = service.cse()
    # https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    search_engine_id = '012608441591405123751:clhx3wq8jxk'
    counter = 0
    start_page = search.last_stop
    logger.debug("Google Search: #request: %s" % num_requests)
    # Make an HTTP request object
    for i1 in range(0, num_requests):
        if search.has_more_results:
            # This is the offset from the beginning to start getting the results from
            start_val = 1 + (start_page * 10)

            # Make an HTTP request object
            # 10 is the maximum & default anyway
            request = collection.list(q=search.string, num=10, start=start_val, cx=search_engine_id )
            response = request.execute()

            for i, doc in enumerate(response['items']):
                try:
                    obj = SearchResult()
                    obj.search = search
                    obj.title = doc.get('title')
                    obj.snippet = doc.get('snippet')
                    obj.url = doc.get('link')
                    obj.rank = start_val + i
                    obj.ifduplicated = False
                    obj.duplicatedto = None
                    obj.save()
                    cache.hincrby('search.%s' % search.id, 'to_process')
                    publish_search_status(obj)
                    do_download.delay(obj.id, obj.url)
                except Exception as e:
                    logger.debug(traceback.format_exc())

            counter = len(response['items'])
            if counter < 10:  # Checks if the results returned are less than actual request of 10
                search.has_more_results = False  # Flag Set no more results

            start_page += 1
            search.last_stop = start_page
            search.save()
        else:
            break
    return 0


@shared_task(default_retry_delay=3, max_retries=3)
def do_download(id, url):
    try:
        data = download(url)
    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.debug("Connection Error: search id %s " % id)
        data = {'path': None, 'doc_type': 'txt', 'text': "Connection Error!", 'raw_html': None}
    obj = SearchResult.objects.get(pk=id)
    obj.raw_file.name = data.get('path')
    obj.doc_type = data.get('doc_type')
    obj.text = data.get('text')
    obj.save()
    obj.raw_html = data.get('raw_html')
    obj.get_nerwords()
    obj.save()

    cache.hincrby('search.%s' % obj.search.id, 'processed')
    publish_search_status(obj)
    return 0


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
            # swampdragon, tell browser one item finishes
            c = 'project_%d_geo' % obj.project.id
            publish_data(c, {"good": 1})
    except Exception, exc:
        raise do_geo_search.retry(exc=exc)


@shared_task(default_retry_delay=3, max_retries=3)
def do_active_filter():
    print "Start Relevance Filter"

    # data base connection
    #CONN_STRING = "host='localhost' dbname='cafi' user='cafi' password='awesome'" #Add this line to local.py
    conn = psycopg2.connect(settings.CONN_STRING)

    # text string to read data
    tf=["text", "title", "snippet"]

    # initial class
    myClf = classifierAPI.Classifier(Tfidf=True, Nwords=5000, classifierMethod='LR')

    # read data from data base
    myClf.readDB(conn, tf)


    # build feature
    features = myClf.buildFeature()

    # show feature ranked by TF
    topWords = myClf.showFeatures()

    print topWords

    # prepare train&test data for model training
    myClf.prepareData()


    # train a model
    myClf.train()


    # prediction on the test data, calculate relevance score
    predictOut = myClf.predict()

    # make recomendation for labeling
    recom = myClf.recommend(predictOut, Nrecommendations=5)

    print recom

    # update database to store the predicted label and relevance score
    myClf.updateDB(conn)
    print "Finished Relevance Filter"


@shared_task(default_retry_delay=3, max_retries=3)
def do_deduplication():
    print "Start Deduplication Filter"

    conn = psycopg2.connect(settings.CONN_STRING)

    tf=["text", "title", "snippet"]

    myClf = classifierAPI.Classifier(Tfidf=True, Nwords=1000)

    myClf.readDB(conn, tf)

    myClf.buildFeature()

    Xtfidf = myClf.features

    srids = myClf.srids

    clusterids = clustering.text_clustering(Xtfidf, method='network', distMetric='cosine', cutval=0.9)

    myClf.updateDuplicationFlags(conn, srids, clusterids)

    print "Finished Deduplication Filter"


if __name__ == '__main__':
    import os, sys
    PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend')
    sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

    from engagement.models import Project
    from google.models import Search, SearchResult
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

    # project = Project(client="xx", name="bbbb")
    # project.save()
    # search = Search(project=project, string='olympic')
    # search.save()
    # do_search(search, 'olympics')
    do_deduplication()
