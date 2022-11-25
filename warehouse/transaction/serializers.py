from rest_framework import serializers

from warehouse.transaction.models import Transaction, TransactionDetail, TransactionReference
from warehouse.transaction.services.transaction_manager import TransactionManager


class ListTransactionReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionReference
        fields = '__all__'


class ListTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date_and_time', 'username']


class ListTransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = '__all__'
        depth = 1


class CreateTransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = ['article', 'quantity', 'reference']


class CreateTransactionSerializer(serializers.ModelSerializer):
    details = CreateTransactionDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['username', 'details']

    def create(self, validated_data):
        details = validated_data.pop('details')
        if len(details) > 0:
            return TransactionManager().create_transaction_and_details_from_validated_data(
                validated_data=validated_data, details=details)
        else:
            return None
