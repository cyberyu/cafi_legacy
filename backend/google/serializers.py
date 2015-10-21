from rest_framework import serializers
from models import Search, SearchResult, GeoSearch
from google.keywords.texthilight import Highlighter


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search


class RiskObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {"risk": value.risk.name,
                "from": value.from_company.name}


class SimpleSearchResultSerializer(serializers.ModelSerializer):
    hltitle = serializers.SerializerMethodField()
    hlsnippet = serializers.SerializerMethodField()

    class Meta:
        model = SearchResult
        fields = ('id', 'hltitle', 'hlsnippet', 'url', 'search')

    def get_hltitle(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        return highlighter.highlight(obj.title, istring)

    def get_hlsnippet(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        return highlighter.highlight(obj.snippet, istring)


class SearchResultSerializer(SimpleSearchResultSerializer):
    hltext = serializers.SerializerMethodField()
    risks = RiskObjectRelatedField(read_only=True, many=True)

    class Meta:
        model = SearchResult

    def get_hltext(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        return highlighter.highlight(obj.text, istring)


class GeoSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSearch



