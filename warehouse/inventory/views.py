import datetime

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import config
from authentication.profile import UserProfile
from core.api_response_message import ApiResponseMessage
from warehouse.inventory import InventoryCycle
from warehouse.inventory.exceptions import InventoryManagerNotCreatedException
from warehouse.inventory.objects import NextInventoryCycle
from warehouse.inventory.serializers import NextInventoryCycleSerializer
from warehouse.inventory.services.inventory_manager import InventoryManager


class CreateInventoryCycleView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        inventory_manager = InventoryManager()
        try:
            inventory_manager.create_inventory_cycle(
                username=UserProfile.objects.get(user__id=request.user.id).username)
        except InventoryManagerNotCreatedException:
            return Response(data=ApiResponseMessage(_('Inventory cycle not created')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ApiResponseMessage(_('Inventory cycle created succesfully')).__dict__,
                        status=status.HTTP_200_OK)


class GetNextInventoryCycle(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NextInventoryCycleSerializer

    def get(self, request, *args, **kwargs):
        last_inventory_cycle = InventoryCycle.objects.first()
        next_inventory_cycle = None
        if last_inventory_cycle is not None:
            next_inventory_cycle = last_inventory_cycle.date + datetime.timedelta(days=config.INVENTORY_CYCLE_DAYS_GAP)

        return Response(status=status.HTTP_200_OK, data=self.serializer_class(
            NextInventoryCycle(last_inventory_cycle=last_inventory_cycle.date if last_inventory_cycle is not None else None,
                               next_inventory_cycle=next_inventory_cycle)).data)
