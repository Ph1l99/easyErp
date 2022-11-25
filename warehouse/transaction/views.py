from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from warehouse.transaction.models import Transaction
from warehouse.transaction.serializers import ListTransactionSerializer, CreateTransactionSerializer


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
