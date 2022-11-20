from django.urls import path

from warehouse.article.views import ArticleListView

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='articles')
]
