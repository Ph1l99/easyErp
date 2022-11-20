from django.db import models


class TransactionReference(models.Model):
    description = models.CharField(max_length=50)
    operation_type = models.CharField(max_length=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description


# class TransactionDetail(models.Model):
#     pass
#
#
# class Transaction(models.Model):
#     pass
