import random
import string

from django.db.models import Count

from repair.models import RepairStatus
from repair.objects import RepairDashboardDetail


class RepairManager:
    @classmethod
    def generate_unique_barcode(cls, length: int):
        return ''.join(random.choices(string.digits, k=length))

    def get_repair_statistics_by_status(self):
        dashboard = []
        repairs = RepairStatus.objects.annotate(total_repairs=Count('repair')).order_by('order')
        for repair in list(repairs):
            dashboard.append(
                RepairDashboardDetail(repair.id, repair.status, repair.class_name, repair.total_repairs).__dict__)
        return dashboard
