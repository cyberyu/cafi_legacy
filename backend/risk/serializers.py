from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from models import Risk, Company, Relation, PredefinedSearch
from models import RiskItem
from google.models import SearchResult


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
    content_type = ContentTypeRelatedField(queryset=RiskItem.objects.all(), required=False)

    class Meta:
        model = RiskItem

    def save(self, **kwargs):
        object_id = self.validated_data.get('object_id')
        content_type = self.validated_data.get('content_type')
        if content_type and object_id:
            content_object = content_type.get_object_for_this_type(pk=object_id)
        super(RiskItemSerializer, self).save(**kwargs)

    def to_representation(self, obj):
        if obj.to_company:
            to_company = obj.to_company.name
        else:
            to_company = ''

        data = {
            "id": obj.id,
            "risk": {"id": obj.risk.id, "name": obj.risk.name},
            "from": {"id": obj.from_company.id, "name": obj.from_company.name},
            # "to": {"id": obj.to_company.id, "name": obj.to_company.name}
        }

        if obj.subrisk:
            data['subrisk'] = {"id": obj.subrisk.id, "name": obj.subrisk.name}

        if obj.content_object:
            data["source"] = {"title": obj.content_object.title, "url": obj.content_object.url}
        elif obj.ex_evidence:
            data["ex_evidence"] = obj.ex_evidence

        return data


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation

    def to_representation(self, obj):
        data = {
            "id": obj.id,
            "buyer": {"id": obj.buyer.id, "name": obj.buyer.name},
            "supplier": {"id": obj.supplier.id, "name": obj.supplier.name},
            "items": obj.items
        }

        if obj.evidence:
            data["evidence"] = {"id": obj.evidence.id, "title": obj.evidence.title, "url": obj.evidence.url}
        elif obj.ex_evidence:
            data["ex_evidence"] = obj.ex_evidence

        return data
