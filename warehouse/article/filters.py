import django_filters.rest_framework as filters

from warehouse.article.models import Article


class ArticleFilter(filters.FilterSet):

    class Meta:
        model = Article
        fields = ['is_active']