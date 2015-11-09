from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route
import csv,json
from djqscsv import render_to_csv_response
from django.http import Http404
from models import Search, SearchResult,GeoSearch
from serializers import SearchSerializer, SearchResultSerializer, GeoSearchSerializer, SimpleSearchResultSerializer
from tasks import do_search, do_geo_search, do_search_single, do_demandsearch
from engagement.models import Project
from celery import chain
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

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
        print "create"
        obj = serializer.save()
        do_search.delay(obj)


    @detail_route(methods=['GET'])
    def highlight(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        search = self.get_object()
        content = do_demandsearch(search,search.last_stop)
        #content = do_search_single(search,search.last_stop) # Download still work in progress
        content = json.loads(content, strict = False)
        return Response(content,status=status.HTTP_201_CREATED)
        #return Response([{"count": "hello, world", "string":"http://time.com/2919041/the-best-moments-of-the-2014-fifa-world-cup/", "id":5}, {"string": "hello1", "count":"bazingaa1 is awesome!" , "id":5}], status=status.HTTP_201_CREATED)

    @list_route(methods=['POST'])
    def batch(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid()
        objs = serializer.save()
        for obj in objs:
            do_search_single.delay(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('search','label',)

    def get_queryset(self):
        queryset = SearchResult.objects.all()
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(search__project=project)
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = SimpleSearchResultSerializer
        return super(SearchResultViewSet, self).list(self, request, *args, **kwargs)


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


class DemandSearch(APIView):
    renderer_classes = (JSONRenderer, )
    def get_object(self, pk):
        try:
            return Search.objects.get(pk=pk)
        except Search.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        search = self.get_object(pk)
        print "Demand:"
        print search
        content = do_demandsearch(search,search.last_stop)
        return Response(content)

class DemandSearchList(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        search = Search.objects.all()
        search = SearchSerializer(search,many=True)
        return Response(search.data)


