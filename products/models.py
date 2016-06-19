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
    sales_price = models.FloatField(
        blank=False,
        null=True
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

    def save(self, *args, **kwargs):
        first_time = not self.pk
        product = super(Product, self).save(*args, **kwargs)
        if first_time:
            for warehouse in Warehouse.objects.filter(owner=self.owner):
                WarehouseStock.objects.create(
                    warehouse=warehouse,
                    product=self,
                    quantity=0.0
                )
            self.save()
        return product
