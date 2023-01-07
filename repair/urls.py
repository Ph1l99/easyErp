from django.urls import path

from repair.views import ListRepairStatusView, ListRepairView, CreateEditGetRepairView, PrintRepairReceipt, \
    PrintRepairLabel, RepairDashboardView

urlpatterns = [
    path('', ListRepairView.as_view(), name='repairs'),
    path('status', ListRepairStatusView.as_view(), name='repair_status'),
    path('dashboard', RepairDashboardView.as_view(), name='repair_dashboard'),
    path('<str:barcode>', CreateEditGetRepairView.as_view(), name='repair'),
    path('<str:barcode>/receipt', PrintRepairReceipt.as_view(), name='repair_receipt'),
    path('<str:barcode>/label', PrintRepairLabel.as_view(), name='repair_label')
]
