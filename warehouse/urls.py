from django.urls import path

from warehouse.article.views import ListArticleView, ArticleView

urlpatterns = [
    path('articles', ListArticleView.as_view(), name='articles'),
    path('articles/<str:barcode>', ArticleView.as_view(), name='article')
]
