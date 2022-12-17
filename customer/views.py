from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.models import Customer, FidelityCard
from customer.serializers import ListCustomerSerializer, ListFidelityCardSerializer, CreateUpdateCustomerSerializer, \
    GetCustomerSerializer


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


class CustomerView(APIView):
    serializer_class = CreateUpdateCustomerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, customer_id):

        try:
            Customer.objects.get(id=customer_id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            try:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = self.serializer_class(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return Response(status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            return Response(data=GetCustomerSerializer(customer).data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
