# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(max_length=100, blank=True)),
                ('rfc', models.CharField(max_length=100, blank=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('cellphone', models.CharField(max_length=20, blank=True)),
                ('address', models.CharField(max_length=254, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'permissions': (),
            },
        ),
    ]
