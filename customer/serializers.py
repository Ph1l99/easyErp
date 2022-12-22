from rest_framework import serializers

from customer.models import Customer, FidelityCard


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

    # todo check if fidelity_card is active and is not assigned to another customer


class GetCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'fidelity_card']

class FidelityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCard
        fields = '__all__'

    # todo check for associated customers if the card is being deactivated