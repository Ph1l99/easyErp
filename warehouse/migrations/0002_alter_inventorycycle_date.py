# Generated by Django 4.1.3 on 2023-01-15 07:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorycycle',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]