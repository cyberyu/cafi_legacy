from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from models import Risk, Company, Relation, PredefinedSearch
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


class PredefinedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedSearch


class CompanySerializer(serializers.ModelSerializer):
    variations = JSONSerializerField(required=False)

    class Meta:
        model = Company
        exclude = ('risks', )


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


class RiskItemSerializer(serializers.ModelSerializer):
    content_object = ContentObjectRelatedField(queryset=RiskItem.objects.all(), required=False)
    content_type = ContentTypeRelatedField(queryset=RiskItem.objects.all())

    class Meta:
        model = RiskItem

    def save(self, **kwargs):
        object_id = self.validated_data.get('object_id')
        content_type = self.validated_data.get('content_type')
        content_object = content_type.get_object_for_this_type(pk=object_id)
        super(RiskItemSerializer, self).save(**kwargs)

    def to_representation(self, obj):
        if obj.to_company:
            to_company = obj.to_company.name
        else:
            to_company = ''

        return {
            'project': obj.project.id,
            'from_company': obj.from_company.name,
            'risk': obj.risk.name,
            'object_id': obj.object_id,
            'content_type': obj.content_type.id,
            'id': obj.id,
            'to_company': to_company,
        }


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation