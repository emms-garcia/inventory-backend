# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-24 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_product_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='eid',
        ),
    ]