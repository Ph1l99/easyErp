from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from warehouse.transaction.models import Transaction, TransactionDetail, TransactionReference
from warehouse.transaction.services.transaction_manager import TransactionManager


class ListTransactionReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionReference
        exclude = ['is_active']


class ListTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date_and_time', 'username']


class ListTransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        exclude = ['transaction']
        depth = 1


class CreateTransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = ['article', 'quantity', 'reference']


class CreateTransactionSerializer(serializers.ModelSerializer):
    details = CreateTransactionDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['details']

    def create(self, validated_data):
        details = validated_data.pop('details')
        if len(details) > 0 and 'username' in self.context:
            transaction_manager = TransactionManager()
            created_transaction = transaction_manager.create_transaction_and_details(
                user_identifier=self.context['username'], details=details)
            transaction_manager.print_labels_for_new_articles(created_transaction)
            return created_transaction
        else:
            raise ValidationError
