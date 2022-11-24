from rest_framework import serializers

from warehouse.transaction.models import Transaction


class ListTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date_and_time', 'username']
