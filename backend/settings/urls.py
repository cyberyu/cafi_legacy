from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from rest_framework import routers
# from rest_framework_extensions.routers import ExtendedSimpleRouter

from google.views import SearchViewSet, SearchResultViewSet, GeoSearchViewSet, upload, DemandSearch, DemandSearchList
from engagement.views import ProjectViewSet
from risk.views import RiskViewSet, CompanyViewSet, RiskItemViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'projects', ProjectViewSet)
router.register(r'gsearch', SearchViewSet)
router.register(r'gdocs', SearchResultViewSet)
#router.register(r'gsearch_update',SearchUpdateViewSet)
#router.register(r'gdocs_update', SearchResultUpdateViewSet)
router.register(r'risks', RiskViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'geosearch', GeoSearchViewSet)
router.register(r'risk_items', RiskItemViewSet)

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls', namespace="core")),
    url(r'^api/', include(router.urls)),
    url(r'^api/upload', 'google.views.upload', name="upload"),
    url(r'^', include('engagement.urls', namespace="project")),
    url(r'^api/DemandSearch/$',DemandSearchList.as_view()),
    url(r'^api/DemandSearch/(?P<pk>[0-9]+)/$',DemandSearch.as_view())
    # url(r'^auth/', include('djoser.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_PATH,
        }),
)

