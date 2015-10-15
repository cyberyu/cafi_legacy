from rest_framework import serializers
from models import Search, SearchResult, GeoSearch
from google.keywords.texthilight import Highlighter


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search


class SearchResultSerializer(serializers.ModelSerializer):
    hltitle = serializers.SerializerMethodField()
    hlsnippet = serializers.SerializerMethodField()

    class Meta:
        model = SearchResult

    def get_hltitle(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        newqstr = istring[:istring.rfind("&")]
        newqstr = newqstr.replace('\"','')
        hiqueryStr= newqstr
        return highlighter.highlight(obj.title,hiqueryStr)
        # return obj.title

    def get_hlsnippet(self, obj):
        highlighter = Highlighter()
        istring = obj.search.string
        newqstr = istring[:istring.rfind("&")]
        newqstr = newqstr.replace('\"','')
        hiqueryStr= newqstr
        return highlighter.highlight(obj.snippet,hiqueryStr)
        # return obj.snippet


class GeoSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSearch



