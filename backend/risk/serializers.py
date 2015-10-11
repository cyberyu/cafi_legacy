from rest_framework import serializers
from models import Risk, Company
from rest_framework import serializers


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk


class CompanySerializer(serializers.ModelSerializer):
    variations = JSONSerializerField(required=False)

    class Meta:
        model = Company