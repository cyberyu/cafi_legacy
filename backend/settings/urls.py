from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from rest_framework import routers
from google.views import SearchViewSet, SearchResultViewSet, GeoSearchViewSet, GeoSearchResultViewSet
from engagement.views import ProjectViewSet
from risk.views import RiskViewSet, CompanyViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'projects', ProjectViewSet)
router.register(r'gsearch', SearchViewSet)
router.register(r'gdocs', SearchResultViewSet)
router.register(r'risks', RiskViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'geosearch', GeoSearchViewSet)
router.register(r'geosearchresult', GeoSearchResultViewSet)


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls', namespace="core")),
    url(r'api/', include(router.urls)),
    url(r'^', include('engagement.urls', namespace="project")),
    # url(r'^auth/', include('djoser.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_PATH,
        }),
)

