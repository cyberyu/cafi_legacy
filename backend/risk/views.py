from rest_framework import viewsets

from models import Company, Risk
from serializers import CompanySerializer, RiskSerializer


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer

    
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer