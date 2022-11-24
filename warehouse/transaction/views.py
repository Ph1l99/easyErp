from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from warehouse.transaction.serializers import ListTransactionSerializer


class ListTransactionView(ListAPIView):
    serializer_class = ListTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
