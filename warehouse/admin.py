from django.contrib import admin

from warehouse.article import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'reorder_threshold')


admin.site.register(Article, ArticleAdmin)
