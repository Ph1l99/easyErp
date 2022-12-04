from django.urls import path

from repair.views import ListRepairStatusView, ListRepairView

urlpatterns = [
    path('', ListRepairView.as_view(), name='repairs'),
    path('status', ListRepairStatusView.as_view(), name='repair_status')
]