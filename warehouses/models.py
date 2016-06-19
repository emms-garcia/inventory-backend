# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Address, Dated


class Warehouse(Address, Dated):
    name = models.CharField(
        blank=True,
        max_length=254,
        null=False)
    description = models.TextField(
        blank=True,
        null=True)
    owner = models.ForeignKey(
        'companies.Company',
        null=True,
        related_name='warehouses')

    REQUIRED_FIELDS = [
        'name', 'owner'
    ]

    class Meta:
        permissions = ()
        verbose_name = 'warehouse'
        verbose_name_plural = 'warehouses'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        return super(Warehouse, self).delete(*args, **kwargs)


class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        null=False,
        related_name='products')
    product = models.ForeignKey(
        'products.Product',
        null=False,
        related_name='stock'
    )
    quantity = models.FloatField(
        default=0.0
    )

    REQUIRED_FIELDS = [
        'warehouse',
        'product',
        'quantity'
    ]

    class Meta:
        permissions = ()
        verbose_name = 'warehouse_stock'
        verbose_name_plural = 'warehouse_stocks'
