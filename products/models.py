# coding: utf-8

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated, EID


class UOM(Dated, EID):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)


class Product(Dated, EID):

    created_by = models.ForeignKey('users.User',
        related_name='products')
    description = models.TextField(
        blank=True,
        null=True)
    name = models.CharField(
        blank=False,
        max_length=100,
        null=False)
    price_per_uom = models.FloatField(
        blank=False,
        default=1.0,
        null=False)
    quantity = models.IntegerField(
        default=0,
        null=False,
        blank=False)
    uom = models.ForeignKey(UOM,
        related_name='products')

    REQUIRED_FIELDS = ['name', 'price_per_uom', 'uom']

    class Meta:
        permissions = ()
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
