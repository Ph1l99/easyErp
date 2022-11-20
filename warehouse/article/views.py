from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from warehouse.article import Article
from warehouse.article.serializers import ArticleSerializer


class ArticleView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(is_active=True)
        if len(articles) > 0:
            return Response(data=self.serializer_class(articles, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
