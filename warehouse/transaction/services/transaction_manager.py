from rest_framework.exceptions import ValidationError

from warehouse.transaction.models import TransactionDetail, Transaction


class TransactionManager:
    def create_transaction_and_details_from_validated_data(self, validated_data, details):

        transaction = Transaction.objects.create(username=validated_data['username'])

        if transaction is not None:
            created_details = []
            for transaction_detail in details:
                try:
                    created_transaction_detail = TransactionDetail.objects.create(article=transaction_detail['article'],
                                                                                  quantity=transaction_detail[
                                                                                      'quantity'],
                                                                                  reference=transaction_detail[
                                                                                      'reference'],
                                                                                  transaction=transaction)
                    # todo check availability in order to provide consistency
                    created_details.append(created_transaction_detail)
                except Exception:
                    if len(created_details) > 0:
                        self._rollback_transaction_detail_creation(created_details=created_details)
                        created_details = []
                        transaction.delete()
                        return None

            return transaction

        return None

    def _rollback_transaction_detail_creation(self, created_details):
        for created_detail in created_details:
            TransactionDetail.objects.filter(id=created_detail.id).delete()
