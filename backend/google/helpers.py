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
        obj.text = """The thing in question was the product of Ahmed’s love of invention. He made the clock out of a metal briefcase-style box, a digital display, wires and a circuit board. It was bigger and bulkier than a typical bedside clock, with cords, screws and electrical components. He said he took it to school on Monday to show an engineering teacher, who said it was nice but then told him he should not show the invention to other teachers. Later, Ahmed’s clock beeped during an English class, and after he revealed the device to the teacher, school officials notified the police, and Ahmed was interrogated by officers. “She thought it was a threat to her,” Ahmed told reporters Wednesday. “So it was really sad that she took a wrong impression of it."""
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

