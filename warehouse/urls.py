from django.urls import path

from warehouse.article.views import ArticleListView, ReadUpdateArticleView

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='articles'),
    path('articles/<str:barcode>', ReadUpdateArticleView.as_view(), name='article')
]
