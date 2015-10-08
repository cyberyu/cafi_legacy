from rest_framework import viewsets

from models import Company, Risk
from serializers import CompanySerializer, RiskSerializer


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer

    
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project', None)
        if project_id:
            return Company.objects.filter(project__id=project_id)
        else:
            return Company.objects.all()



