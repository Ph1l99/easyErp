from django.db import models
from django.utils import timezone

from warehouse.article import Article


class TransactionReference(models.Model):
    OPERATION_TYPE = [
        ('+', 'LOAD'),
        ('-', 'UNLOAD')
    ]
    description = models.CharField(max_length=50)
    operation_type = models.CharField(max_length=1, choices=OPERATION_TYPE, default='+')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['id']


class Transaction(models.Model):
    date_and_time = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=20)

    def __str__(self):
        return 'Trans. id: ' + str(self.id) + ' - Time: ' + self.date_and_time.strftime('%d-%m-%-yT%H:%M:%S')

    class Meta:
        ordering = ['-id']


class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    reference = models.ForeignKey(TransactionReference, on_delete=models.RESTRICT)

    def __str__(self):
        return 'Trans. detail: ' + str(self.id)
