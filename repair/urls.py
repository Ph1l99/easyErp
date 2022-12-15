from django.urls import path

from repair.views import ListRepairStatusView, ListRepairView, CreateEditGetRepairView, PrintRepairReceipt

urlpatterns = [
    path('', ListRepairView.as_view(), name='repairs'),
    path('status', ListRepairStatusView.as_view(), name='repair_status'),
    path('<str:barcode>', CreateEditGetRepairView.as_view(), name='repair'),
    path('<str:barcode>/receipt', PrintRepairReceipt.as_view(), name='repair')
]