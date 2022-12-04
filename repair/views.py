from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from repair.models import RepairStatus, Repair
from repair.serializers import RepairStatusSerializer, ListRepairSerializer, RepairSerializer


class ListRepairStatusView(ListAPIView):
    serializer_class = RepairStatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    queryset = RepairStatus.objects.all()


class ListRepairView(ListAPIView):
    serializer_class = ListRepairSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    queryset = Repair.objects.all()


class CreateEditGetRepairView(APIView):
    serializer_class = RepairSerializer

    def get(self, request, barcode):
        try:
            repair = Repair.objects.get(barcode=barcode)
            return Response(self.serializer_class(repair).data, status=status.HTTP_200_OK)
        except Repair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, barcode):
        pass

    def put(self, request, barcode):
        pass

    def delete(self, request, barcode):
        pass
