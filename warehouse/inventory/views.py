from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.profile import UserProfile
from warehouse.inventory.exceptions import InventoryManagerNotCreatedException
from warehouse.inventory.services.inventory_manager import InventoryManager


class CreateInventoryCycleView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        inventory_manager = InventoryManager()
        try:
            inventory_manager.create_inventory_cycle(username=UserProfile.objects.get(user__id=request.user.id).username)
        except InventoryManagerNotCreatedException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
