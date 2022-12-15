from django.db import models


class FidelityCard(models.Model):
    barcode = models.CharField(max_length=50, primary_key=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.barcode


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    fidelity_card = models.ForeignKey(FidelityCard, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return ' '.join([self.last_name, self.first_name])

    class Meta:
        ordering = ['last_name']
