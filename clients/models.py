# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated


class Client(Dated):
    address = models.CharField(
        blank=True,
        max_length=254,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    company = models.CharField(
        blank=True,
        max_length=100,
        null=True
    )
    email = models.EmailField(
        max_length=254
    )
    latitude = models.FloatField(
        blank=True,
        null=True
    )
    longitude = models.FloatField(
        blank=True,
        null=True
    )
    name = models.CharField(
        blank=True,
        max_length=100,
        null=False)
    owner = models.ForeignKey(
        'users.User',
        related_name='clients'
    )
    phone = models.CharField(
        blank=True,
        max_length=20,
        null=True
    )
    rfc = models.CharField(
        blank=True,
        max_length=100,
        null=True
    )

    REQUIRED_FIELDS = ['name', 'company', 'owner']

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return self.name
