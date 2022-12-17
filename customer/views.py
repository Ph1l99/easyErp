from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from customer.models import Customer, FidelityCard
from customer.serializers import ListCustomerSerializer, ListFidelityCardSerializer


class ListCustomerView(ListAPIView):
    serializer_class = ListCustomerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']
    queryset = Customer.objects.all()


class ListFidelityCardView(ListAPIView):
    serializer_class = ListFidelityCardSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    queryset = FidelityCard.objects.all()
