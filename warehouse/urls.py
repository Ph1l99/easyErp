from django.urls import path

from warehouse.article.views import ListArticleView, ArticleView, PrintArticleLabel, ArticleDashboardView
from warehouse.inventory.views import CreateInventoryCycleView, GetNextInventoryCycle
from warehouse.transaction.views import ListTransactionView, CreateTransactionView, ListTransactionReferenceView, \
    ListTransactionDetailsView

urlpatterns = [
    path('articles', ListArticleView.as_view(), name='articles'),
    path('articles/dashboard', ArticleDashboardView.as_view(), name='articles_dashboard'),
    path('articles/<str:barcode>', ArticleView.as_view(), name='article'),
    path('articles/<str:barcode>/label', PrintArticleLabel.as_view(), name='article_label')
]

urlpatterns += [
    path('transactions', ListTransactionView.as_view(), name='transactions'),
    path('transactions/-1', CreateTransactionView.as_view(), name='transaction'),
    path('transactions/<int:transaction_id>/details', ListTransactionDetailsView.as_view(), name='transaction_details'),
    path('transactions/references', ListTransactionReferenceView.as_view(), name='transactions_references')
]

urlpatterns += [
    path('inventory/cycle', CreateInventoryCycleView.as_view(), name='inventory_cycle'),
    path('inventory/cycle/next', GetNextInventoryCycle.as_view(), name='next_inventory_cycle')
]
