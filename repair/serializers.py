from rest_framework import serializers

from repair.models import RepairStatus, Repair


class RepairStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairStatus
        fields = '__all__'


class ListRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'
        depth = 1
