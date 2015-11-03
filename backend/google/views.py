from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route
import csv
from djqscsv import render_to_csv_response

from models import Search, SearchResult,GeoSearch
from serializers import SearchSerializer, SearchResultSerializer, GeoSearchSerializer, SimpleSearchResultSerializer
from tasks import do_search, do_geo_search, do_search_single
from engagement.models import Project
from celery import chain


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
        obj = serializer.save()
        #do_search.delay(obj,obj.last_stop)
        do_search.delay(obj)

    def perform_update(self, serializer):
        obj1 = serializer.save()
        print "update: "+ obj1.search
        if obj1.flag_check == 0:
            do_search_single.delay(obj1,obj1.last_stop)
        else:
            print "No results left"

    @list_route(methods=['POST'])
    def batch(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid()
        objs = serializer.save()
        for obj in objs:
            do_search.delay(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SearchUpdateViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project',)

    def perform_update(self, serializer):
        obj1 = serializer.save()
        print "update: "+ obj1.search
        if obj1.flag_check == 0:
            do_search_single.delay(obj1,obj1.last_stop)
        else:
            print "No results left"



class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('search','label')

    def get_queryset(self):
        queryset = SearchResult.objects.all()
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(search__project=project)
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = SimpleSearchResultSerializer
        return super(SearchResultViewSet, self).list(self, request, *args, **kwargs)

class SearchResultUpdateViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('search','label')

    def get_queryset(self):
        queryset = SearchResult.objects.all()
        project = self.request.query_params.get('project', None)
        string = self.request.query_params.get('string', None)
        if project is not None and string is not None:
            queryset = queryset.filter(search__project=project)
            queryset = queryset.filter(search__string=string)
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = SimpleSearchResultSerializer
        return super(SearchResultUpdateViewSet, self).list(self, request, *args, **kwargs)


class GeoSearchViewSet(viewsets.ModelViewSet):
    queryset = GeoSearch.objects.all()
    serializer_class = GeoSearchSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project__id', 'name')

    def perform_create(self, serializer):
        geosearch = serializer.save()
        print geosearch.address
        print "doing geo search create"
        do_geo_search.delay(geosearch.id, geosearch.address)

    def perform_update(self, serializer):
        geosearch = serializer.save()
        print "update: "+ geosearch.address
        do_geo_search.delay(geosearch.id, geosearch.address)

    @detail_route(methods=['POST'])
    def batch(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        proj = Project.objects.get(pk=project_id)
        count = 0

        for item in request.data:
            item.update({"project": project_id})
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data.get('address').strip() and (not serializer.validated_data.get('lat')):
                self.perform_create(serializer)
                count += 1
        headers = self.get_success_headers(serializer.data)
        return Response({"count": count}, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=['GET'])
    def download(self, request, *args, **kwargs):

        project_id = self.kwargs['pk']
        items = GeoSearch.objects.filter(project__id=project_id)

        qs = GeoSearch.objects.filter(project__id=project_id).values('name', 'address', 'lat', 'lng', 'status')
        return render_to_csv_response(qs)



@api_view(['POST'])
def upload(request):
    file = request.data.get('file')
    data = list(csv.DictReader(file))

    return Response({"items": data}, status=status.HTTP_200_OK)

