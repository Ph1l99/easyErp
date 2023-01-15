from django.db import models
from django.utils import timezone

from warehouse.article.models import Article


class InventoryCycle(models.Model):
    date = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=20)

    def __str__(self):
        return 'Inv. cycle: ' + str(self.id) + ' date: ' + self.date.strftime('%d-%m-%-y')

    class Meta:
        ordering = ['-date']


class InventoryCycleDetail(models.Model):
    article = models.ForeignKey(Article, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=0)
    cycle = models.ForeignKey(InventoryCycle, on_delete=models.CASCADE)

    def __str__(self):
        return 'Id: ' + str(self.id) + ' article: ' + str(self.article.barcode) + ' qty: ' + str(self.quantity)
