from rest_framework import serializers
from models import Search, SearchResult


class SearchSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(read_only=True, view_name='project-detail')
    class Meta:
        model = Search


class SearchResultSerializer(serializers.ModelSerializer):
    search = serializers.HyperlinkedRelatedField(read_only=True, view_name='search-detail')
    class Meta:
        model = Search

 