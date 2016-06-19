# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated


class ProductGroup(Dated):
    description = models.TextField(
        blank=True,
        null=True)
    name = models.CharField(
        blank=False,
        max_length=100,
        null=False)
    owner = models.ForeignKey(
        'companies.Company',
        null=True,
        related_name='product_groups'
    )

    REQUIRED_FIELDS = ['name', 'owner']

    class Meta:
        permissions = ()
        verbose_name = 'product_group'
        verbose_name_plural = 'product_groups'

    def __str__(self):
        return self.name

class GroupProduct(models.Model):
    group = models.ForeignKey(
        ProductGroup,
        related_name='products'
    )
    product = models.ForeignKey(
        'products.Product',
        related_name='group_products'
    )
    quantity = models.FloatField(
        blank=False,
        default=1.0,
        null=False
    )

    REQUIRED_FIELDS = ['group', 'product', 'quantity']

    class Meta:
        permissions = ()
        verbose_name = 'group_product'
        verbose_name_plural = 'group_products'

    def __str__(self):
        return self.name
