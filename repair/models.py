from django.db import models
from django.utils import timezone

from customer.models import Customer


class RepairStatus(models.Model):
    status = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    class_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.status

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Repair statuses'


class Repair(models.Model):
    barcode = models.CharField(primary_key=True, max_length=60)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1200)
    delivery_date = models.DateField(blank=True, null=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(RepairStatus, on_delete=models.RESTRICT)
    insert_date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.barcode

    class Meta:
        ordering = ['-insert_date_time']
