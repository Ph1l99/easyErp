from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from repair.models import RepairStatus
from repair.serializers import RepairStatusSerializer


class ListRepairStatusView(ListAPIView):
    serializer_class = RepairStatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    queryset = RepairStatus.objects.all()
