# coding: utf-8

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated, EID


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
    price_per_unit = models.FloatField(
        blank=False,
        default=1.0,
        null=False)
    quantity = models.FloatField(
        blank=False,
        default=1.0,
        null=False)

    REQUIRED_FIELDS = ['name', 'price_per_unit', 'quantity']

    class Meta:
        permissions = ()
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
