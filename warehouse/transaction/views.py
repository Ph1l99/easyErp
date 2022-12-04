from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from warehouse.transaction.exceptions import TransactionQuantityNotConsistentException
from warehouse.transaction.models import Transaction, TransactionReference, TransactionDetail
from warehouse.transaction.serializers import ListTransactionSerializer, CreateTransactionSerializer, \
    ListTransactionReferenceSerializer, ListTransactionDetailsSerializer


class ListTransactionDetailsView(APIView):
    serializer_class = ListTransactionDetailsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get(self, request, transaction_id):
        if Transaction.objects.filter(id=transaction_id).exists():
            return Response(self.serializer_class(TransactionDetail.objects.filter(transaction__id=transaction_id),
                                                  many=True).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ListTransactionView(ListAPIView):
    serializer_class = ListTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    queryset = Transaction.objects.all()


class CreateTransactionView(CreateAPIView):
    serializer_class = CreateTransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='One or more submitted parameters are incorrect')
        except TransactionQuantityNotConsistentException:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='Some items do have an inconsistent quantity. Transaction not saved')
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='Error while processing transaction')


class ListTransactionReferenceView(ListAPIView):
    serializer_class = ListTransactionReferenceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    queryset = TransactionReference.objects.all()
