# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-24 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('warehouses', '0003_auto_20160524_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='companies.Company'),
        ),
    ]
