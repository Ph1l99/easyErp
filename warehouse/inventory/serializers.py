from rest_framework import serializers


class NextInventoryCycleSerializer(serializers.Serializer):
    last_inventory_cycle = serializers.DateField()
    next_inventory_cycle = serializers.DateField()
