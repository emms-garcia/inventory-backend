# coding: utf-8

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated


class ProductGroup(Dated):

    created_by = models.ForeignKey('users.User',
        related_name='product_groups')
    description = models.TextField(
        blank=True,
        null=True)
    name = models.CharField(
        blank=False,
        max_length=100,
        null=False)

    REQUIRED_FIELDS = ['name']

    class Meta:
        permissions = ()
        verbose_name = 'product_group'
        verbose_name_plural = 'product_groups'

    def __str__(self):
        return self.name

class GroupProduct(models.Model):
    group = models.ForeignKey(ProductGroup,
        related_name='products')
    product = models.ForeignKey('products.Product',
        related_name='group_products')
    quantity = models.IntegerField(
        blank=False,
        default=1,
        null=False)

    REQUIRED_FIELDS = ['name', 'group', 'product', 'quantity']

    class Meta:
        permissions = ()
        verbose_name = 'group_product'
        verbose_name_plural = 'group_products'

    def __str__(self):
        return self.name