from rest_framework import serializers

from customer.exceptions import FidelityCardAlreadyAssignedException
from customer.models import Customer, FidelityCard
from customer.services.fidelity_card_service import FidelityCardService


class ListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'fidelity_card']


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
        if fidelity_card_service.is_fidelity_card_available(validated_data.get('fidelity_card')):
            return self.create(**validated_data)

    def update(self, instance, validated_data):
        fidelity_card_service = FidelityCardService()
        if fidelity_card_service.is_fidelity_card_available(validated_data.get('fidelity_card')):
            return self.update(instance, validated_data)


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
                return self.create(**validated_data)

    def update(self, instance, validated_data):
        fidelity_card_service = FidelityCardService()
        fidelity_card_status = validated_data.get('is_active')
        if not fidelity_card_status:
            if not fidelity_card_service.is_fidelity_card_linked_to_customer(validated_data.get('barcode')):
                return self.update(instance, validated_data)
