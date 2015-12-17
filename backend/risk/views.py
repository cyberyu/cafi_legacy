from rest_framework import viewsets
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from models import Company, Risk, RiskItem, Relation, PredefinedSearch
from engagement.models import Project
import csv
from google.permissions import ValidateSessionAuthentication

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
    authentication_classes = (ValidateSessionAuthentication,)


class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    authentication_classes = (ValidateSessionAuthentication,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('evidence', 'buyer', 'supplier')
