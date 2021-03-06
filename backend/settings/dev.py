"""
Django settings for search_tool project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import redis
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR-SECRET-KEY-HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_nose',
    'djcelery',
    'swampdragon',
    'engagement',
    'google',
    'risk',
    'core',
    # 'tag_store'  # for future use with cr_complaint_analytics_core
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.core.context_processors.request',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LoginRequiredMiddleware',
)

LOGIN_URL = '^$'
LOGIN_EXEMPT_URLS = (
        r'^register/',
        r'^login/',
        r'^static/',
        r'^me/',
        r'^admin/'
)

LOG_PATHS = (
    '/_search',
    '/_export',
    '/_save_search',
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=google, request_logger',
]

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
# APPEND_SLASH = True


VALID_DOMAINS = ['']

ES_HOST = 'http://localhost:9200' #default Elasticsearch setting
ES_INDEX = 'YOUR-ES-INDEX-HERE'
ES_TYPE = 'YOUR-ES-TYPE-HERE'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend','rest_framework.filters.OrderingFilter','rest_framework.filters.SearchFilter',),
    'DEFAULT_PARSER_CLASSES': (
        # 'rest_framework.parsers.JSONParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        # 'rest_framework.renderers.JSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.AdminRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 20
}

#python manage.py celery beat : Starting celerybeat is similar to starting a worker. Start another window, set up your Django environment

CACHE = redis.Redis(host='localhost', port=6379)
TIKA_SERVER = 'http://localhost:9998'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' #storing the schedules in a Django database table

CELERY_ROUTES = {
    'google.tasks.do_search': {
        'queue': 'search_q'
    },
    'google.tasks.do_download': {
        'queue': 'download_q'
    },
    'google.tasks.do_geo_search': {
        'queue': 'geo_q'
    },
    'google.tasks.do_active_filter':{
        'queue': 'act_q'
    }
}

############## SWAMPDRAGON ##################
SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')
DRAGON_URL = 'http://localhost:9999/'
#############################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "{%(asctime)s}[%(levelname)s] %(message)s",
        },
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug1.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console','file'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console','file'],
            'level': 'WARN',
            'propagate': True,
        },
        'CAFI': {
            'handlers': ['console','file'],
            'level': 'DEBUG',
        },
    }
}

from settings.local import *
