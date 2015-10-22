from rest_framework import serializers
from models import Search, SearchResult, GeoSearch
from google.keywords.texthilight import Highlighter
from google.CustomSearchAPI.searchParser import SearchQueryParser
from google.ner.cafi_netagger import CAFI_NETagger


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
    risks = RiskObjectRelatedField(read_only=True, many=True)
    keywords = serializers.SerializerMethodField()
    nerwords = serializers.SerializerMethodField()

    class Meta:
        model = SearchResult

    def get_keywords(self, obj):
        parser = SearchQueryParser()
        return parser.Parse(obj.search.string)

    def get_nerwords(self, obj):
        nt = CAFI_NETagger()  # intialize the tagger
        nt.get_ne_tags_all(obj.text)  # tag the text
        return {"person": set(nt.get_ne_tags_PERSON()),
                "org": set(nt.get_ne_tags_ORGANIZATION()),
                "location": set(nt.get_ne_tags_LOCATION())}

class GeoSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSearch



