from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.easy_erp_page_number_pagination import EasyErpPageNumberPagination
from core.printing.exceptions import PrinterDoesNotExistException
from core.printing.usb_label_printer import UsbLabelPrinter
from core.printing.usb_thermal_printer import UsbThermalPrinter
from repair.models import RepairStatus, Repair
from repair.serializers import RepairStatusSerializer, ListRepairSerializer, RepairSerializer


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
    filterset_fields = ['status']
    queryset = Repair.objects.all()


class CreateEditGetRepairView(APIView):
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, barcode):
        try:
            repair = Repair.objects.get(barcode=barcode)
            return Response(self.serializer_class(repair).data, status=status.HTTP_200_OK)
        except Repair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, barcode):
        try:
            Repair.objects.get(barcode=barcode)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Repair.DoesNotExist:
            try:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                repair = serializer.save()
                # todo print label and receipt
                return Response(data=self.serializer_class(repair).data, status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, barcode):
        try:
            article_to_be_updated = Repair.objects.get(barcode=barcode)
            serializer = self.serializer_class(article_to_be_updated, data=request.data)
            serializer.is_valid(raise_exception=True)
            repair = serializer.save()
            return Response(data=self.serializer_class(repair).data, status=status.HTTP_200_OK)
        except Repair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, barcode):
        try:
            repair = Repair.objects.get(barcode=barcode)
            repair.delete()
        except Repair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PrintRepairReceipt(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, barcode):
        try:
            thermal_printer = UsbThermalPrinter()
            Repair.objects.get(barcode=barcode)
            thermal_printer.print_repair_receipt(barcode=barcode)
        except Repair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PrinterDoesNotExistException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class PrintRepairLabel(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, barcode):
        try:
            thermal_printer = UsbLabelPrinter()
            Repair.objects.get(barcode=barcode)
            thermal_printer.print_label(barcode=barcode)
        except Repair.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PrinterDoesNotExistException:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
