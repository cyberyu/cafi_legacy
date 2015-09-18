from rest_framework import viewsets

from models import Search, SearchResult 
from serializers import SearchSerializer, SearchResultSerializer
from helpers import do_search

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


