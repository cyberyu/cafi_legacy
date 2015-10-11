from rest_framework import serializers
from models import Search, SearchResult, GeoSearch


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search


class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult


class GeoSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSearch


