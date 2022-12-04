from warehouse.article import Article
from warehouse.inventory import InventoryCycle, InventoryCycleDetail
from warehouse.transaction import TransactionDetail


class InventoryManager:
    def create_inventory_cycle(self, username):
        inventory_cycle_creation_result = True
        articles_for_new_inventory_cycle = []

        # Loop over active articles and get current quantity
        for article in Article.objects.filter(is_active=True).all():
            articles_for_new_inventory_cycle.append((article, self.get_current_quantity_for_article(article.barcode)))

        # Create new inventory cycle
        new_inventory_cycle = InventoryCycle.objects.create(username=username)

        # For each article a new inventory cycle detail is created
        for article, new_quantity in articles_for_new_inventory_cycle:
            try:
                InventoryCycleDetail.objects.create(article=article, quantity=new_quantity, cycle=new_inventory_cycle)
            except Exception:
                # If an exception occurs, the whole inventory cycle is rolled back
                inventory_cycle_creation_result = False
                InventoryCycle.delete(new_inventory_cycle)
                break

        return inventory_cycle_creation_result

    def get_current_quantity_for_article(self, barcode):
        # Initialize starting quantity (i.e. quantity for a specific article from the very beginning)
        starting_quantity = 0
        # Initialize partial quantity (i.e. quantity since last inventory cycle)
        partial_quantity = 0
        # Initialize the last transactions list
        transactions_for_article = []

        # Retrieve last inventory cycle
        last_inventory_cycle = InventoryCycle.objects.first()
        if last_inventory_cycle is not None:
            # If an inventory cycle is present, the starting quantity is set with the last quantity that has been computed
            starting_quantity = InventoryCycleDetail.objects.get(cycle=last_inventory_cycle).quantity
            transactions_for_article = TransactionDetail.objects.filter(article__barcode=barcode,
                                                                        transaction__date_and_time__gt=last_inventory_cycle.date)

        if len(transactions_for_article) > 0:
            for transaction in transactions_for_article:
                partial_quantity += int(transaction.reference.operation_type + str(transaction.quantity))

        return starting_quantity + partial_quantity
