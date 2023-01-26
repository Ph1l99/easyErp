import logging

from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api_response_message import ApiResponseMessage
from core.easy_erp_page_number_pagination import EasyErpPageNumberPagination
from core.printing.exceptions import PrinterDoesNotExistException, PrinterErrorException
from core.printing.usb_label_printer import UsbLabelPrinter
from core.printing.usb_receipt_printer import UsbReceiptPrinter
from repair.models import RepairStatus, Repair
from repair.serializers import RepairStatusSerializer, ListRepairSerializer, RepairSerializer, RepairDashboardSerializer
from repair.services.repair_manager import RepairManager

logger = logging.getLogger(__name__)


class ListRepairStatusView(ListAPIView):
    serializer_class = RepairStatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    queryset = RepairStatus.objects.all()


class ListRepairView(ListAPIView):
    serializer_class = ListRepairSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = EasyErpPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'customer']
    queryset = Repair.objects.all()


class CreateEditGetRepairView(APIView):
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, barcode):
        try:
            repair = Repair.objects.get(barcode=barcode)
            return Response(self.serializer_class(repair).data, status=status.HTTP_200_OK)
        except Repair.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Repair not found')).__dict__, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, barcode):
        try:
            Repair.objects.get(barcode=barcode)
            return Response(data=ApiResponseMessage(_('Repair already exists')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        except Repair.DoesNotExist:
            try:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                repair = serializer.save()
                try:
                    receipt_printer = UsbReceiptPrinter()
                    label_printer = UsbLabelPrinter()
                    receipt_printer.print_repair_receipt(barcode=repair.barcode)
                    label_printer.print_label(barcode_string=repair.barcode)
                except PrinterDoesNotExistException or PrinterErrorException or Exception:
                    logger.error('Unable to print repair label or receipt. Printer not exists or input data not valid')
                return Response(data=self.serializer_class(repair).data, status=status.HTTP_201_CREATED)
            except ValidationError:
                logger.error('Error while validating repair data')
                return Response(data=ApiResponseMessage(_('Error while parsing request')).__dict__,
                                status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, barcode):
        try:
            article_to_be_updated = Repair.objects.get(barcode=barcode)
            serializer = self.serializer_class(article_to_be_updated, data=request.data)
            serializer.is_valid(raise_exception=True)
            repair = serializer.save()
            return Response(data=self.serializer_class(repair).data, status=status.HTTP_200_OK)
        except Repair.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Unable to edit. Repair not found')).__dict__,
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(data=ApiResponseMessage(_('Error while parsing request')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, barcode):
        try:
            repair = Repair.objects.get(barcode=barcode)
            repair.delete()
            return Response(status=status.HTTP_200_OK)
        except Repair.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Unable to delete. Repair not found')).__dict__,
                            status=status.HTTP_404_NOT_FOUND)


class PrintRepairReceipt(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, barcode):
        try:
            receipt_printer = UsbReceiptPrinter()
            Repair.objects.get(barcode=barcode)
            receipt_printer.print_repair_receipt(barcode=barcode)
        except Repair.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Unable to print receipt. Repair not found')).__dict__,
                            status=status.HTTP_404_NOT_FOUND)
        except PrinterDoesNotExistException:
            logger.error('Printer not initialized')
            return Response(data=ApiResponseMessage(_('Receipt printer not available')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        except PrinterErrorException:
            logger.error('Printer error. Print rejected')
            return Response(data=ApiResponseMessage(_('Error while printing receipt')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ApiResponseMessage(_('Receipt printed successfully')).__dict__, status=status.HTTP_200_OK)


class PrintRepairLabel(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, barcode):
        try:
            label_printer = UsbLabelPrinter()
            Repair.objects.get(barcode=barcode)
            label_printer.print_label(barcode_string=barcode)
        except Repair.DoesNotExist:
            return Response(data=ApiResponseMessage(_('Unable to print label. Repair not found')).__dict__,
                            status=status.HTTP_404_NOT_FOUND)
        except PrinterDoesNotExistException:
            logger.error('Printer not initialized')
            return Response(data=ApiResponseMessage(_('Label printer not available')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        except PrinterErrorException:
            logger.error('Printer error. Print rejected')
            return Response(data=ApiResponseMessage(_('Error while printing label')).__dict__,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data=ApiResponseMessage(_('Label printed successfully')).__dict__, status=status.HTTP_200_OK)


class RepairDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RepairDashboardSerializer

    def get(self, request):
        try:
            dashboard_data = self.serializer_class(
                data={'dashboard': RepairManager().get_repair_statistics_by_status()})
            dashboard_data.is_valid(raise_exception=True)
            return Response(data=dashboard_data.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
