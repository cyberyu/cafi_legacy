from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route
import csv,json
from djqscsv import render_to_csv_response
from models import Search, SearchResult,GeoSearch
from serializers import SearchSerializer, SearchResultSerializer, GeoSearchSerializer, SimpleSearchResultSerializer
from tasks import do_search, do_geo_search
from engagement.models import Project
from celery import chain
from rest_framework.response import Response

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
    filter_fields = ('project',)

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        do_search.delay(obj,3)

    @detail_route(methods=['GET'])
    def demand_page(self, request, *args, **kwargs):

        search = self.get_object()
        logger.debug("Demand Fetch")
        demo = do_search.delay(search,1)
        demo.get()
        return Response({"Get_one_more_page": "Completed"},status=status.HTTP_201_CREATED)

        """
        # This part was for visualization of results of 10 fetched docs in the api itself:

        obj1 = SearchResult.objects.all().filter(search=search.pk).order_by('-rank')[0]
        rank_last = obj1.rank
        logger.debug("Rank_Last:"+str(rank_last))
        demo = do_search.delay(search,1)
        demo.get()
        obj = SearchResult.objects.all().filter(search=search.pk).filter(rank__gt=rank_last).order_by('rank')
        if len(obj)>0:
            results = []
            for res in obj:
                results.append(SimpleSearchResultSerializer(res).data)

            results1 = json.dumps(results)
            results2 = json.loads(results1,strict = False)
            return Response(results2, status=status.HTTP_201_CREATED)
        else:
            return Response(None,status=status.HTTP_201_CREATED)
        """


    @list_route(methods=['POST'])
    def batch(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid()
        objs = serializer.save()
        for obj in objs:
            do_search.delay(obj,3)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchResultViewSet(viewsets.ModelViewSet):
    queryset = SearchResult.objects.all()
    serializer_class = SearchResultSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('search','label', 'user')

    def get_queryset(self):
        queryset = SearchResult.objects.all()
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(search__project=project)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        logger.debug("Address :"+ geosearch.address)
        logger.debug("Geo Create")
        do_geo_search.delay(geosearch.id, geosearch.address)

    def perform_update(self, serializer):
        geosearch = serializer.save()
        logger.debug("update: "+ geosearch.address)
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
