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
    print_labels = serializers.BooleanField(default=False)

    class Meta:
        model = Transaction
        fields = ['details', 'print_labels']

    def create(self, validated_data):
        details = validated_data.pop('details')
        print_labels = validated_data.pop('print_labels')
        if len(details) > 0 and 'username' in self.context:
            transaction_manager = TransactionManager()
            created_transaction = transaction_manager.create_transaction_and_details(
                user_identifier=self.context['username'], details=details)
            if print_labels:
                transaction_manager.print_labels_for_new_articles(created_transaction)
            return created_transaction
        else:
            raise ValidationError
