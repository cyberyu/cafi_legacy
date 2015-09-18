from googleapiclient.discovery import build

if __name__ == '__main__':
    import os, sys
    PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend')
    sys.path.append(PROJECT_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

from google.models import Search, SearchResult

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
    from engagement.models import Project
    from google.models import Search, SearchResult
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()

    project = Project(client="xx", name="bbbb")
    project.save()
    search = Search(project=project, string='olympic')
    search.save()
    do_search(search, 'olympics')

