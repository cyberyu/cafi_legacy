from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls', namespace="core")),
    url(r'^', include('engagement.urls', namespace="project")),
    url(r'^', include('google.urls', namespace="google")),
    # url(r'^auth/', include('djoser.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_PATH,
        }),
)