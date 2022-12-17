from rest_framework import serializers

from customer.models import Customer, FidelityCard


class ListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']


class ListFidelityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCard
        fields = '__all__'


class CreateUpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'fidelity_card']


class GetCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1
