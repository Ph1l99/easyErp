import random
import string

from warehouse.article.models import Article
from warehouse.inventory.services.inventory_manager import InventoryManager


class ArticleManager:
    @classmethod
    def generate_unique_barcode(cls, length: int):
        return ''.join(random.choices(string.digits, k=length))

    @classmethod
    def get_count_articles_current_availability_equal_zero(cls):
        zero_availability_articles = 0
        articles = Article.objects.filter(is_active=True).all()
        for article in articles:
            if InventoryManager().get_current_quantity_for_article(article.barcode) == 0:
                zero_availability_articles += 1
        return zero_availability_articles

    @classmethod
    def get_count_articles_current_availability_below_reorder(cls):
        below_reorder_threshold_articles = 0
        articles = Article.objects.filter(is_active=True).all()
        for article in articles:
            if InventoryManager().get_current_quantity_for_article(article.barcode) < article.reorder_threshold:
                below_reorder_threshold_articles += 1
        return below_reorder_threshold_articles
