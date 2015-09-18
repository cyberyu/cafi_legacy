from rest_framework import serializers
from models import Risk, Company


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company