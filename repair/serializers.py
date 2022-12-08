from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import config
from repair.models import RepairStatus, Repair
from repair.services.repair_manager import RepairManager


class RepairStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairStatus
        fields = '__all__'


class ListRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'
        depth = 1


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('barcode') == '-1':

            generated_barcode = RepairManager.generate_unique_barcode(length=config.ARTICLE_BARCODE_LENGTH)

            while Repair.objects.filter(barcode=generated_barcode).exists():
                generated_barcode = RepairManager.generate_unique_barcode(length=10)

            article = Repair.objects.create(barcode=generated_barcode,
                                            title=validated_data.get('title'),
                                            description=validated_data.get('description'),
                                            delivery_date=validated_data.get('delivery_date'),
                                            customer=validated_data.get('customer'),
                                            customer_phone=validated_data.get('customer'),
                                            status=validated_data.get('status'))
        else:
            raise ValidationError
        return article
