from rest_framework import viewsets

from models import Search, SearchResult 
from serializers import SearchSerializer, SearchResultSerializer


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer    

    
class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer    