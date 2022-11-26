from django.db import models
from django.utils import timezone

from warehouse.article import Article


class InventoryCycle(models.Model):
    date = models.DateField(default=timezone.now)
    username = models.CharField(max_length=20)


class InventoryCycleDetail(models.Model):
    article = models.ForeignKey(Article, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=0)
    cycle = models.ForeignKey(InventoryCycle, on_delete=models.RESTRICT)
