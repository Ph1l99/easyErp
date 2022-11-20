from django.contrib import admin

from warehouse.article import Article
from warehouse.transaction.models import TransactionReference


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'reorder_threshold')


class TransactionReferenceAdmin(admin.ModelAdmin):
    list_display = ('description', 'operation_type', 'is_active')


admin.site.register(Article, ArticleAdmin)
admin.site.register(TransactionReference, TransactionReferenceAdmin)
