from rest_framework import serializers
from models import Search, SearchResult, GeoSearch
from google.keywords.texthilight import Highlighter
from google.CustomSearchAPI.searchParser import SearchQueryParser
from google.ner.cafi_netagger import CAFI_NETagger
from risk.serializers import RelationSerializer

class SearchSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Search


class RiskObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if value.subrisk:
            return {"id": value.risk.id,
                    "risk": {"id": value.risk.id, "name": value.risk.name},
                    "subrisk": {"id": value.subrisk.id, "name": value.subrisk.name},
                    "from": {"id": value.from_company.id, "name": value.from_company.name},
                    # "to": {"id": value.to_company.id, "name": value.to_company.name}
                    }
        else:
            return {"id": value.risk.id,
                    "risk": {"id": value.risk.id, "name": value.risk.name},
                    "from": {"id": value.from_company.id, "name": value.from_company.name},
                    # "to": {"id": value.to_company.id, "name": value.to_company.name}
                    }


class SimpleSearchResultSerializer(serializers.ModelSerializer):
    hltitle = serializers.SerializerMethodField()
    hlsnippet = serializers.SerializerMethodField()

    class Meta:
        model = SearchResult
        fields = ('id', 'hltitle', 'hlsnippet', 'url', 'search','relevance', 'predicted_relevance', 'predicted_score', 'rank')

    def get_hltitle(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        return highlighter.highlight(obj.title, istring)

    def get_hlsnippet(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        return highlighter.highlight(obj.snippet, istring)


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""
    def to_internal_value(self, data):
        return data
    def to_representation(self, value):
        return value


class SearchResultSerializer(SimpleSearchResultSerializer):
    risks = RiskObjectRelatedField(read_only=True, many=True)
    relations = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    # nerwords = serializers.SerializerMethodField()
    nerwords = JSONSerializerField(required=False)

    class Meta:
        model = SearchResult

    def get_keywords(self, obj):
        parser = SearchQueryParser()
        return parser.Parse(obj.search.string)

    def get_relations(self, obj):
        return RelationSerializer(obj.relations, many=True).data


class GeoSearchSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')
    class Meta:
        model = GeoSearch


