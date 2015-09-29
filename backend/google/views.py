from rest_framework import viewsets

from models import Search, SearchResult,GeoSearch,GeoSearchResult
from serializers import SearchSerializer, SearchResultSerializer, GeoSearchSerializer, GeoSearchResultSerializer
from helpers import do_search, do_geo_search

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer

    def perform_create(self, serializer):
        print serializer.data
        search_obj = serializer.save()
        print "doing search"
        do_search(search_obj, serializer.data.get('string'))


class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer


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

