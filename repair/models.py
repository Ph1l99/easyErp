from django.db import models
from django.utils import timezone


class RepairStatus(models.Model):
    status = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Repair statuses'


class Repair(models.Model):
    barcode = models.CharField(primary_key=True, max_length=60)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1200)
    delivery_date = models.DateField(blank=True, null=True)
    customer = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=30)
    status = models.ForeignKey(RepairStatus, on_delete=models.RESTRICT)
    insert_date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.barcode

    class Meta:
        ordering = ['-insert_date_time']
