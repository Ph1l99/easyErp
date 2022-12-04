from rest_framework import serializers

from repair.models import RepairStatus


class RepairStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepairStatus
        fields = '__all__'