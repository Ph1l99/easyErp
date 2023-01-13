# Generated by Django 4.1.3 on 2023-01-13 13:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40)),
                ('is_active', models.BooleanField(default=True)),
                ('class_name', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Repair statuses',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('barcode', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1200)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('insert_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='repair.repairstatus')),
            ],
            options={
                'ordering': ['-insert_date_time'],
            },
        ),
    ]
