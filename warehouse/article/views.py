from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from warehouse.article import Article
from warehouse.article.serializers import ArticleSerializer


class ArticleView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, barcode):
        try:
            article = Article.objects.get(barcode=barcode)
            return Response(data=self.serializer_class(article).data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, barcode):
        try:
            Article.objects.get(barcode=barcode)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

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
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'barcode']
    queryset = Article.objects.all()
