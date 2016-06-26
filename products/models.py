# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated
from warehouses.models import Warehouse, WarehouseStock


class Product(Dated):
    description = models.TextField(
        blank=True,
        null=True
    )
    name = models.CharField(
        blank=False,
        max_length=100,
        null=False
    )
    owner = models.ForeignKey(
        'companies.Company',
        null=True,
        related_name='products'
    )
    price = models.FloatField(
        blank=False,
        default=1.0,
        null=False
    )
    price_per_unit = models.FloatField(
        blank=False,
        null=True
    )
    uom = models.ForeignKey(
        'uoms.UOM',
        null=True
    )
    quantity = models.FloatField(
        default=0.0
    )

    REQUIRED_FIELDS = [
        'name',
        'price'
    ]

    class Meta:
        permissions = ()
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
