from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from models import Risk, Company
from models import RiskItem
from google.models import SearchResult
from google.serializers import SearchResultSerializer


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


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, SearchResult):
            # serializer = SearchResultSerializer(value)
            return value.id
        else:
            raise Exception('Unexpected type of tagged object')
        # return serializer.data

class ContentTypeRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return ContentType.objects.get(model=data)

    def to_representation(self, value):
        return value.name

class RiskRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return Risk.objects.get(pk=data)

    def to_representation(self, value):
        return value.name

class CompanyRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return Company.objects.get(pk=data)

    def to_representation(self, value):
        return value.name

class RiskItemSerializer(serializers.ModelSerializer):
    content_object = ContentObjectRelatedField(queryset=RiskItem.objects.all(), required=False)
    content_type = ContentTypeRelatedField(queryset=RiskItem.objects.all())
    risk = RiskRelatedField(queryset=RiskItem.objects.all())
    from_company = CompanyRelatedField(queryset=RiskItem.objects.all())
    to_company = CompanyRelatedField(queryset=RiskItem.objects.all(), required=False)

    class Meta:
        model = RiskItem
        # fields = ('risk', 'project', 'from_company', 'to_company', 'object_id', 'content_object')

    def save(self, **kwargs):
        object_id = self.validated_data.get('object_id')
        content_type = self.validated_data.get('content_type')
        content_object = content_type.get_object_for_this_type(pk=object_id)
        super(RiskItemSerializer, self).save(**kwargs)
