# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 01:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_groups', '0002_auto_20160328_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_products', to='products.Product'),
        ),
    ]
