from django.urls import path

from warehouse.article.views import ListArticleView, ReadUpdateArticleView

urlpatterns = [
    path('articles', ListArticleView.as_view(), name='articles'),
    path('articles/<str:barcode>', ReadUpdateArticleView.as_view(), name='article')
]
