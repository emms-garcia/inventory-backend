# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-28 01:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_groups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupproduct',
            name='description',
        ),
        migrations.RemoveField(
            model_name='groupproduct',
            name='name',
        ),
    ]
