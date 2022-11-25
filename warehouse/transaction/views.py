from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from warehouse.transaction.models import Transaction, TransactionReference
from warehouse.transaction.serializers import ListTransactionSerializer, CreateTransactionSerializer, \
    ListTransactionReferenceSerializer


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
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ListTransactionReferenceView(ListAPIView):
    serializer_class = ListTransactionReferenceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    queryset = TransactionReference.objects.all()
