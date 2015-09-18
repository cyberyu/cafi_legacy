import sys
import os 

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../backend')
sys.path.append(PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")

from engagement.models import Project
from google.models import Search, SearchResult

# this will create a Search object, and save it to database used by Django
# search = Search(project=1, string='')
# doc = SearchResult(search=search, title='', url='', snippet='')
# doc.save()
