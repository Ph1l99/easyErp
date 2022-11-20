import datetime

from django.db import models


class TransactionReference(models.Model):
    description = models.CharField(max_length=50)
    operation_type = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description


class TransactionDetail(models.Model):
    article_identifier = models.CharField(max_length=60)
    quantity = models.IntegerField(default=1)
    reference = models.ForeignKey(TransactionReference, on_delete=models.RESTRICT, blank=True)

    def __str__(self):
        return self.id


class Transaction(models.Model):
    details = models.ManyToManyField(TransactionDetail, related_name='transaction')
    date_and_time = models.DateTimeField(default=datetime.datetime.utcnow())
    username = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id) + ' - ' + self.date_and_time.strftime('%d-%m-%-yT%H:%M:%S')
