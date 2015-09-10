from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^_search/save', 'cr_search.views.save_search', name='save_search'),
    url(r'^_search/get', 'cr_search.views.get_saved_search', name='get_saved_search'),
    url(r'^_search', 'cr_search.views.search', name='search'),
    url(r'^_export', 'cr_search.views.export', name='export'),
    url(r'^_suggest', 'cr_search.views.suggest', name='suggest'),
    # url(r'^item/(?P<id>[0-9]+)/$', 'cr_search.views.item', name='item'),
    url(r'^document/(?P<id>[0-9]+)/$', 'cr_search.views.document', name='document'),
)
