from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api_response_message import ApiResponseMessage
from core.easy_erp_page_number_pagination import EasyErpPageNumberPagination
from core.printing.exceptions import PrinterDoesNotExistException, PrinterErrorException
from core.printing.usb_label_printer import UsbLabelPrinter
from warehouse.article.models import Article
from warehouse.article.objects import ArticleDashboardDetail
from warehouse.article.serializers import ArticleSerializer, ArticleDashboardSerializer
from warehouse.article.services.article_manager import ArticleManager


class ArticleView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, barcode):
        try:
            article = Article.objects.get(barcode=barcode)
            return Response(data=self.serializer_class(article).data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Article not found')).__dict__, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, barcode):
        try:
            Article.objects.get(barcode=barcode)
            return Response(data=ApiResponseMessage(_('Article already exists')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            try:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                article = serializer.save()
                return Response(data=self.serializer_class(article).data, status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(data=ApiResponseMessage(_('Error while parsing request')).__dict__,
                                status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, barcode):
        try:
            article_to_be_updated = Article.objects.get(barcode=barcode)
            serializer = self.serializer_class(article_to_be_updated, data=request.data)
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            return Response(data=self.serializer_class(article).data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Article not found')).__dict__, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(data=ApiResponseMessage(_('Error while parsing request')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)


class ListArticleView(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = EasyErpPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'barcode']
    queryset = Article.objects.all()


class PrintArticleLabel(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, barcode):
        try:
            label_printer = UsbLabelPrinter()
            Article.objects.get(barcode=barcode)
            label_printer.print_label(barcode_string=barcode)
        except Article.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Unable to print label. Article not found')).__dict__,
                            status=status.HTTP_404_NOT_FOUND)
        except PrinterDoesNotExistException:
            return Response(data=ApiResponseMessage(_('Label printer not available')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        except PrinterErrorException:
            return Response(data=ApiResponseMessage(_('Error while printing label')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ApiResponseMessage(_('Label printed successfully')).__dict__, status=status.HTTP_200_OK)


class ArticleDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleDashboardSerializer

    def get(self, request):
        article_manager = ArticleManager()

        no_availability_label = _('No availability')
        low_availability_label = _('Low availability')

        count_articles_availability_zero = ArticleDashboardDetail(label=no_availability_label,
                                                                  value=article_manager.get_count_articles_current_availability_equal_zero()).__dict__
        count_articles_availability_below_reorder_threshold = ArticleDashboardDetail(
            label=low_availability_label,
            value=article_manager.get_count_articles_current_availability_below_reorder()).__dict__
        try:
            dashboard = self.serializer_class(data={'dashboard': [count_articles_availability_zero,
                                                                  count_articles_availability_below_reorder_threshold]})
            dashboard.is_valid(raise_exception=True)
            return Response(data=dashboard.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
