# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'complaints',
#         'USER': 'svc_search',
#         'PASSWORD': 'search',
#     }
# }
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR+'/dev1'
	}
}

SECRET_KEY = '95=bj+!@1#ryx91n0@^tsycv!6#_yevken1l!*#jw9wu6k7pxp'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_URL = '/Users/pengfeiz/Projects/cafi/static/' 
STATIC_PATH = '/Users/pengfeiz/Projects/cafi/static/'
STATIC_ROOT = '/Users/pengfeiz/Projects/cafi/static/'

