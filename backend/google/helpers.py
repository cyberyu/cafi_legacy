import googlemaps
from googleapiclient.discovery import build
from google.alchemyapi_python.alchemyapi import AlchemyAPI
from google.models import Search, SearchResult, GeoSearch, GeoSearchResult
import json


class GeocodingTest():
    def __init__(self):
        self.key = 'AIzaSyC8viCWyzR_q2MBKLeRZGpc7BHA3NTNimA' #Autocafi Developer Key
        self.client = googlemaps.Client(self.key)

    def simple_geocode(self,query):
        results = self.client.geocode(query)
        return results
        #print json.dumps(results, indent=1)
        
def extract_text_AlchemyAPI_single(url_string):

    alchemyapi = AlchemyAPI()
    response1 = alchemyapi.text('url', url_string)
    if response1['status'] == 'OK':
        try:
            #print (unicode(response1['text']))
            return unicode(response1['text'])
        except:

            pass

    else:
        return None


def test_api(url_string):
    return url_string


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
        obj.text = extract_text_AlchemyAPI_single(doc.get('link'))
        obj.save()


def do_geo_search(search, string):
    query = GeocodingTest()
    results = query.simple_geocode(string)
    result = results[0]["geometry"]["location"]
    obj = GeoSearchResult()
    obj.search = search
    obj.lat = result.get('lat')
    obj.lng = result.get('lng')
    obj.save()



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

