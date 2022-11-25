from django.contrib import admin

from warehouse.article import Article
from warehouse.transaction.models import TransactionReference, Transaction, TransactionDetail


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'reorder_threshold')


class TransactionReferenceAdmin(admin.ModelAdmin):
    list_display = ('description', 'operation_type', 'is_active')


class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'quantity', 'reference')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_and_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(TransactionReference, TransactionReferenceAdmin)
admin.site.register(TransactionDetail, TransactionDetailAdmin)
admin.site.register(Transaction, TransactionAdmin)
