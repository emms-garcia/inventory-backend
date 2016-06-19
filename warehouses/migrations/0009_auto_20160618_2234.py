# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-18 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20160524_0157'),
        ('warehouses', '0008_warehouse_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='warehousestock',
            options={'permissions': (), 'verbose_name': 'warehouse_stock', 'verbose_name_plural': 'warehouse_stocks'},
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='created_by',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='companies.Company'),
        ),
    ]
