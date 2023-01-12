from rest_framework import serializers

from customer.models import Customer, FidelityCard
from customer.services.fidelity_card_service import FidelityCardService


class ListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ListFidelityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCard
        fields = '__all__'


class CreateUpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'fidelity_card']

    def create(self, validated_data):
        fidelity_card_service = FidelityCardService()
        if fidelity_card_service.is_fidelity_card_available(validated_data.get('fidelity_card', None)):
            return Customer.objects.create(**validated_data)


def update(self, instance, validated_data):
    fidelity_card_service = FidelityCardService()
    if fidelity_card_service.is_fidelity_card_available(validated_data.get('fidelity_card', None)):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.fidelity_card = validated_data.get('fidelity_card', instance.fidelity_card)
        instance.save()
        return instance


class GetCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'fidelity_card']


class FidelityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCard
        fields = '__all__'

    def create(self, validated_data):
        fidelity_card_service = FidelityCardService()
        fidelity_card_status = validated_data.get('is_active')
        if not fidelity_card_status:
            if not fidelity_card_service.is_fidelity_card_linked_to_customer(validated_data.get('barcode')):
                return FidelityCard.objects.create(**validated_data)
        else:
            return FidelityCard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        fidelity_card_service = FidelityCardService()
        fidelity_card_status = validated_data.get('is_active')
        if not fidelity_card_status:
            if not fidelity_card_service.is_fidelity_card_linked_to_customer(validated_data.get('barcode')):
                instance.is_active = validated_data.get('is_active', instance.is_active)
                instance.barcode = validated_data.get('barcode', instance.barcode)
                instance.save()
                return instance
        else:
            instance.is_active = validated_data.get('is_active', instance.is_active)
            instance.barcode = validated_data.get('barcode', instance.barcode)
            instance.save()
            return instance
