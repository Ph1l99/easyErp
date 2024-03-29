# Generated by Django 4.1.3 on 2023-01-13 13:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('barcode', models.CharField(max_length=60, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('reorder_threshold', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InventoryCycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('username', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TransactionReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('operation_type', models.CharField(choices=[('+', 'LOAD'), ('-', 'UNLOAD')], default='+', max_length=1)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='warehouse.article')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='warehouse.transactionreference')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryCycleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='warehouse.article')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.inventorycycle')),
            ],
        ),
    ]
