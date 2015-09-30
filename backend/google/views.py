from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from models import Search, SearchResult,GeoSearch,GeoSearchResult
from serializers import SearchSerializer, SearchResultSerializer, GeoSearchSerializer, GeoSearchResultSerializer
from helpers import do_search, do_geo_search


class ResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project',)

    def perform_create(self, serializer):
        print serializer.data
        search_obj = serializer.save()
        print "doing search"
        do_search(search_obj, serializer.data.get('string'))


class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('search',)

    def get_queryset(self):
        queryset = SearchResult.objects.all()
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(search__project=project)
        return queryset


class GeoSearchViewSet(viewsets.ModelViewSet):
    queryset = GeoSearch.objects.all()
    serializer_class = GeoSearchSerializer
    def perform_create(self, serializer):
        search_obj = serializer.save()
        print search_obj
        print "doing geo search"
        do_geo_search(search_obj, serializer.data.get('string'))


class GeoSearchResultViewSet(viewsets.ModelViewSet):
    queryset = GeoSearchResult.objects.all()
    serializer_class = GeoSearchResultSerializer

