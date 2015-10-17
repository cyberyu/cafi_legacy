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
    # 'core.middleware.LoginRequiredMiddleware',
)

LOGIN_URL = '/login/'
LOGIN_EXEMPT_URLS = (
        r'^register/',
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
    'DEFAULT_PARSER_CLASSES': (
        # 'rest_framework.parsers.JSONParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        # 'rest_framework.renderers.JSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.AdminRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 20
}

CACHE = redis.Redis(host='localhost', port=6379)

from settings.local import *
