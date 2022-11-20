from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from warehouse.article import Article
from warehouse.article.serializers import ArticleSerializer


class ReadUpdateArticleView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, barcode):
        try:
            article = Article.objects.get(barcode=barcode)
            return Response(data=self.serializer_class(article).data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, barcode):
        if not Article.objects.filter(barcode=barcode).exists():
            try:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid()
                serializer.save()
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, barcode):
        try:
            article_to_be_updated = Article.objects.get(barcode=barcode)
            serializer = self.serializer_class(article_to_be_updated, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ListArticleView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(is_active=True)
        if articles.exists():
            return Response(data=self.serializer_class(articles, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
