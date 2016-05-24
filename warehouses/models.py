# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Address, Dated, EID


class Warehouse(Address, Dated, EID):

    created_by = models.ForeignKey(
        'users.User',
        related_name='warehouses')
    name = models.CharField(
        blank=True,
        max_length=254,
        null=False)
    contact = models.ForeignKey(
        'users.User',
        null=True)
    owner = models.ForeignKey(
        'companies.Company',
        related_name='warehouses'
    )


    REQUIRED_FIELDS = [
        'created_by', 'name', 'owner'
    ]

    class Meta:
        permissions = ()
        verbose_name = 'warehouse'
        verbose_name_plural = 'warehouses'

    def __str__(self):
        return self.name

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
        verbose_name_plural = 'warehouse_stock'
