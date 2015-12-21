from rest_framework import viewsets
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework_csv import renderers as csv_r
from django.http import HttpResponse
from djqscsv import render_to_csv_response
from collections import OrderedDict
from models import Company, Risk, RiskItem, Relation, PredefinedSearch
from engagement.models import Project
import csv
from google.permissions import ValidateSessionAuthentication
from filters import RelationFilter, RiskItemFilter

from serializers import CompanySerializer, RiskSerializer, \
    RiskItemSerializer, RelationSerializer, PredefinedSearchSerializer


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name','type')
    authentication_classes = (ValidateSessionAuthentication,)


class PredefinedSearchViewSet(viewsets.ModelViewSet):
    queryset = PredefinedSearch.objects.all()
    serializer_class = PredefinedSearchSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name','is_global')
    authentication_classes = (ValidateSessionAuthentication,)

    
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('project',)
    authentication_classes = (ValidateSessionAuthentication,)

    def get_queryset(self):
        project_id = self.request.query_params.get('project', None)
        if project_id:
            return Company.objects.filter(project__id=project_id)
        else:
            return Company.objects.all()

    @detail_route(methods=['POST'])
    def upload(self, request, *args, **kwargs):

        project_id = self.kwargs['pk']
        project = Project.objects.get(pk=project_id)

        file = request.data.get('file')
        data = list(csv.DictReader(file))
        for item in data:
            item['variations'] = [v.strip() for v in item.get('variations').split(';')]
            item['project'] = project_id;
            serializer = CompanySerializer(data=item)
            serializer.is_valid()
            company = serializer.save()
            # company.project_set.add(project)

        queryset = Company.objects.filter(project__id=project_id);
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RiskItemViewSet(viewsets.ModelViewSet):
    queryset = RiskItem.objects.all()
    serializer_class = RiskItemSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('project', 'from_company', 'to_company', 'risk', 'subrisk')
    filter_class = RiskItemFilter
    ordering_fields = ('from_company', 'risk', 'subrisk')

    authentication_classes = (ValidateSessionAuthentication,)

    @detail_route(methods=['GET'])
    def download(self, request, *args, **kwargs):

        project_id = self.kwargs['pk']
        qs = RiskItem.objects.filter(project__id=project_id)
        data = RiskItemSerializer(qs, many=True).data

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="risks-%s.csv"' % project_id

        results = []
        for item in data:
            new_item = OrderedDict([
                ("From company", item["from"]["name"]),
                ("Risk", item["risk"]["name"]),
                ("Sub risk", item.get('subrisk', {}).get('name', None)),
                ("source.title", item.get("source", {}).get("title", None)),
                ("source.url", item.get("source", {}).get("url", None)),
                ("external source", item.get('ex_evidence', None))
            ])
            results.append(new_item)

        writer = csv.writer(response)
        if len(results) > 0:
            writer.writerow(results[0].keys())
        for row in results:
            writer.writerow(row.values())

        return response


class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    authentication_classes = (ValidateSessionAuthentication,)
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_fields = ('project', 'evidence', 'buyer', 'supplier')
    filter_class = RelationFilter
    ordering_fields = ('buyer__name', 'supplier__name')

    @detail_route(methods=['GET'])
    def download(self, request, *args, **kwargs):

        project_id = self.kwargs['pk']
        qs = Relation.objects.filter(project__id=project_id)
        data = RelationSerializer(qs, many=True).data

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relations-%s.csv"' % project_id

        results = []
        for item in data:
            new_item = OrderedDict([
                ("buyer", item["buyer"]["name"]),
                ("supplier", item["supplier"]["name"]),
                ("items", item["items"]),
                ("source.title", item.get("evidence", {}).get("title", None)),
                ("source.url", item.get("evidence", {}).get("url", None)),
                ("external source", item.get('ex_evidence', None))
            ])
            results.append(new_item)

        writer = csv.writer(response)
        if len(results) > 0:
            writer.writerow(results[0].keys())
        for row in results:
            writer.writerow(row.values())

        return response
