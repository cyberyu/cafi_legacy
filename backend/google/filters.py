__author__ = 'tanmoy'

import django_filters

from models import GeoSearch

class GeoSearchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    address = django_filters.CharFilter(name="address", lookup_type=("icontains"))
    class Meta:
        model = GeoSearch
        fields = ['name', 'address']


