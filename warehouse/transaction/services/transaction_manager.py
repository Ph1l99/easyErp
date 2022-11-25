from rest_framework.exceptions import ValidationError

from warehouse.transaction.models import TransactionDetail, Transaction


class TransactionManager:
    def create_transaction_and_details_from_validated_data(self, validated_data, details):
        created_details = []
        for transaction_detail in details:
            try:
                created_transaction_detail = TransactionDetail.objects.create(article=transaction_detail['article'],
                                                                              quantity=transaction_detail[
                                                                                  'quantity'],
                                                                              reference=transaction_detail[
                                                                                  'reference'])
                created_details.append(created_transaction_detail)
            except ValidationError:
                if len(created_details) > 0:
                    self._rollback_transaction_detail_creation(created_details=created_details)
                    created_details = []

        if len(created_details) > 0:
            transaction = Transaction.objects.create(username=validated_data['username'])
            transaction.details.set(created_details)
            return transaction

        return None

    def _rollback_transaction_detail_creation(self, created_details):
        for created_detail in created_details:
            TransactionDetail.objects.filter(id=created_detail.id).delete()
