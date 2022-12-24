from rest_framework import serializers


class NextInventoryCycleSerializer(serializers.Serializer):
    last_inventory_cycle = serializers.DateTimeField()
    next_inventory_cycle = serializers.DateTimeField()
