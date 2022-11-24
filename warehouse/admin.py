from django.contrib import admin

from warehouse.article import Article
from warehouse.transaction.models import TransactionReference, Transaction


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'reorder_threshold')


class TransactionReferenceAdmin(admin.ModelAdmin):
    list_display = ('description', 'operation_type', 'is_active')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_and_time')


admin.site.register(Article, ArticleAdmin)
admin.site.register(TransactionReference, TransactionReferenceAdmin)
admin.site.register(Transaction, TransactionAdmin)
