from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^_search/save', 'google.views.save_search', name='save_search'),
    url(r'^_search/get', 'google.views.get_saved_search', name='get_saved_search'),
    url(r'^_search', 'google.views.search', name='search'),
    url(r'^_export', 'google.views.export', name='export'),
    url(r'^_suggest', 'google.views.suggest', name='suggest'),
    url(r'^document/(?P<id>[0-9]+)/$', 'google.views.document', name='document'),
)
