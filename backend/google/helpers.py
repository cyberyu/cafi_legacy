
from googleapiclient.discovery import build

from models import Search, SearchResult


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
        obj.save()


if __name__ == '__main__':
    do_search(1, 'olympics')

