from django.urls import path

from warehouse.article.views import ArticleListView, ArticleView

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='articles'),
    path('articles/<str:barcode>', ArticleView.as_view(), name='article')
]
