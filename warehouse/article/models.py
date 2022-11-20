from django.db import models


class Article(models.Model):
    barcode = models.CharField(primary_key=True, max_length=60, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    reorder_threshold = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
