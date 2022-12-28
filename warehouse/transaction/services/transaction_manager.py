from warehouse.inventory.services.inventory_manager import InventoryManager
from warehouse.transaction.exceptions import TransactionQuantityNotConsistentException
from warehouse.transaction.models import TransactionDetail, Transaction


class TransactionManager:
    def create_transaction_and_details(self, user_identifier, details):

        transaction = Transaction.objects.create(username=user_identifier)

        if transaction is not None:
            for transaction_detail in details:
                # todo maybe we check that only active articles may be transacted
                # Extract the current article quantity and the one being transacted
                current_quantity_for_article = InventoryManager().get_current_quantity_for_article(
                    transaction_detail['article'].barcode)
                quantity_being_transacted = int(
                    transaction_detail['reference'].operation_type + str(transaction_detail['quantity']))

                if self._is_quantity_consistent(current_quantity=current_quantity_for_article,
                                                quantity_being_transacted=quantity_being_transacted):
                    TransactionDetail.objects.create(article=transaction_detail['article'],
                                                     quantity=transaction_detail[
                                                         'quantity'],
                                                     reference=transaction_detail[
                                                         'reference'],
                                                     transaction=transaction)
                else:
                    # If the quantity is not consistent, the whole transaction is rolled back
                    transaction.delete()
                    raise TransactionQuantityNotConsistentException
            return transaction

        raise Transaction.DoesNotExist

    def _is_quantity_consistent(self, current_quantity, quantity_being_transacted):
        return quantity_being_transacted != 0 and \
            (current_quantity <= 0 and
             current_quantity + quantity_being_transacted > current_quantity) or \
            (current_quantity >= 0 and
             current_quantity + quantity_being_transacted >= 0)
