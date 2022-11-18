from django.db import models

from authentication.user.models import User


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

