from django_filters import rest_framework as filters

from customer.models import FidelityCard


class FidelityCardFilter(filters.FilterSet):
    is_available = filters.BooleanFilter(field_name='customer', lookup_expr='isnull')

    class Meta:
        model = FidelityCard
        fields = ['is_active']
