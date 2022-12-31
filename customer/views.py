from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.easy_erp_page_number_pagination import EasyErpPageNumberPagination
from customer.exceptions import FidelityCardAlreadyAssignedException
from customer.filters import FidelityCardFilter
from customer.models import Customer, FidelityCard
from customer.serializers import ListCustomerSerializer, ListFidelityCardSerializer, CreateUpdateCustomerSerializer, \
    GetCustomerSerializer, FidelityCardSerializer


class ListCustomerView(ListAPIView):
    serializer_class = ListCustomerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = EasyErpPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'fidelity_card__barcode']
    queryset = Customer.objects.all()


class ListFidelityCardView(ListAPIView):
    serializer_class = ListFidelityCardSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = EasyErpPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = FidelityCardFilter
    search_fields = ['barcode']
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
                customer = serializer.save()
                return Response(data=GetCustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except FidelityCardAlreadyAssignedException:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = self.serializer_class(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            saved_customer = serializer.save()
            return Response(data=GetCustomerSerializer(saved_customer).data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except FidelityCardAlreadyAssignedException:
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


class FidelityCardView(APIView):
    serializer_class = FidelityCardSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, barcode):
        try:
            FidelityCard.objects.get(barcode=barcode)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except FidelityCard.DoesNotExist:
            try:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                fidelity_card = serializer.save()
                return Response(data=self.serializer_class(fidelity_card).data, status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            except FidelityCardAlreadyAssignedException:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, barcode):
        try:
            fidelity_card = FidelityCard.objects.get(barcode=barcode)
            serializer = self.serializer_class(fidelity_card, data=request.data)
            serializer.is_valid(raise_exception=True)
            saved_fidelity_card = serializer.save()
            return Response(data=self.serializer_class(saved_fidelity_card).data, status=status.HTTP_200_OK)
        except FidelityCard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except FidelityCardAlreadyAssignedException:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, barcode):
        try:
            fidelity_card = FidelityCard.objects.get(barcode=barcode)
            return Response(self.serializer_class(fidelity_card).data, status=status.HTTP_200_OK)
        except FidelityCard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
