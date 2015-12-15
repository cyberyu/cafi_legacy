from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route,authentication_classes
import csv,json
from djqscsv import render_to_csv_response
from models import Search, SearchResult,GeoSearch
from serializers import SearchSerializer, SearchResultSerializer, GeoSearchSerializer, SimpleSearchResultSerializer
from tasks import do_search, do_geo_search, do_active_filter
from engagement.models import Project
from celery import chain
from rest_framework.response import Response
from google.permissions import ValidateSessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
import time

import logging
logger = logging.getLogger("CAFI")

class ResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project', 'user', 'is_relevant')
    authentication_classes = (ValidateSessionAuthentication,)

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        user_val = self.request.user
        logger.debug("Create Search: " +str(user_val))
        do_search.delay(obj, 3)

    @detail_route(methods=['POST'])
    def demand_page(self, request, *args, **kwargs):
        search = self.get_object()
        logger.debug("Demand Fetch")
        do_search.delay(search, 1)
        return Response({"msg": "submitted"}, status=status.HTTP_201_CREATED)

    @list_route(methods=['POST'])
    def batch(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid()
        objs = serializer.save(user=request.user)
        for obj in objs:
            do_search.delay(obj, 3)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields = ('search', 'label', 'review_later', 'search__project')
    ordering_fields = ('rank', 'predicted_score','relevance')
    authentication_classes = (ValidateSessionAuthentication,)

    def get_queryset(self):
        queryset = SearchResult.objects.all()
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(search__project=project)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        self.serializer_class = SimpleSearchResultSerializer
        return super(SearchResultViewSet, self).list(self, request, *args, **kwargs)

class GeoSearchViewSet(viewsets.ModelViewSet):
    queryset = GeoSearch.objects.all()
    serializer_class = GeoSearchSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project', 'name', 'user')
    authentication_classes = (ValidateSessionAuthentication,)

    def perform_create(self, serializer):
        logger.debug("Geo Create")
        geosearch = serializer.save(user=self.request.user)
        logger.debug("Address :"+ geosearch.address)
        result = do_geo_search.delay(geosearch.id, geosearch.address)


    def perform_update(self, serializer):
        geosearch = serializer.save()
        logger.debug("update: "+ geosearch.address)
        result = do_geo_search.delay(geosearch.id, geosearch.address)
        time.sleep(5)
        if result.ready():
            print "Task has run"
            if result.successful():
                print "Result was: %s" % result.result
            else:
                if isinstance(result.result, Exception):
                    print "Task failed due to raising an exception"
                    raise result.result
                else:
                    print "Task failed without raising exception"
        else:
            print "Task has not yet run"

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

class Upload(APIView):
    authentication_classes = (ValidateSessionAuthentication,)
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request, format=None):
        file = request.data.get('file')
        data = list(csv.DictReader(file))

        return Response({"items": data}, status=status.HTTP_200_OK)

#@api_view(['GET'])
#def upload(request):
#    file = request.data.get('file')
#    data = list(csv.DictReader(file))

#    return Response({"items": data}, status=status.HTTP_200_OK)

class Relevancefilter(APIView):
    authentication_classes = (ValidateSessionAuthentication,)
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request, format=None):
        logger.debug("Starting Relevance Filtering")
        do_active_filter.delay()
        return Response({"Hello": "World"}, status=status.HTTP_200_OK)
