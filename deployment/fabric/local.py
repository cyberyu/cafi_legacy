# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cafi',
        'USER': 'cafi',
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# DATABASES = {
#  'default': {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': BASE_DIR+'/dev1'
#  }
# }

SECRET_KEY = '95=bj+!@1#ryx91n0@^tsycv!6#_yevken1l!*#jw9wu6k7pxp'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_URL = '/Users/yangm/cafi/project/static/' 
STATIC_PATH = '/Users/yangm/cafi/project/static/'
STATIC_ROOT = '/Users/yangm/cafi/project/static/'