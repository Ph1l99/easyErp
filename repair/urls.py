from django.urls import path

from repair.views import ListRepairStatusView

urlpatterns = [
    path('status', ListRepairStatusView.as_view(), name='repair_status')
]