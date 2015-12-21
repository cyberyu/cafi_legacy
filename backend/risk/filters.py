__author__ = 'tanmoy'

import django_filters

from models import Relation, RiskItem

class RelationFilter(django_filters.FilterSet):
    buyer = django_filters.CharFilter(name="buyer__name", lookup_type=("icontains"))
    supplier = django_filters.CharFilter(name="supplier__name", lookup_type=("icontains"))
    items = django_filters.CharFilter(name="items", lookup_type=("icontains"))

    class Meta:
        model = Relation


class RiskItemFilter(django_filters.FilterSet):
    risk = django_filters.CharFilter(name="risk__name", lookup_type=("icontains"))
    from_company = django_filters.CharFilter(name="from_company__name", lookup_type=("icontains"))
    subrisk = django_filters.CharFilter(name="subrisk__name", lookup_type=("icontains"))

    class Meta:
        model = RiskItem
