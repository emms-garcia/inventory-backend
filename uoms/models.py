# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated


class UOM(Dated):
    name = models.CharField(
        blank=True,
        max_length=254,
        null=False
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    short_name = models.CharField(
        blank=True,
        max_length=42,
        null=False
    )
    owner = models.ForeignKey(
        'companies.Company',
        null=True,
        related_name='uoms'
    )

    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'uom'
        verbose_name_plural = 'uoms'

    def __str__(self):
        return self.name
