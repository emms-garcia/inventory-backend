# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated


class Transaction(Dated):
    client = models.ForeignKey(
        'clients.Client',
        null=True,
        related_name='transactions'
    )
    created_by = models.ForeignKey(
        'users.User',
        null=False,
        related_name='transactions'
    )
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
        null=False,
        related_name='transactions'
    )
    type = models.CharField(
        blank=False,
        null=False,
        max_length=10
    )
    voucher = models.TextField(
        blank=False,
        null=False,
        default='{}')

    REQUIRED_FIELDS = [
        'created_by',
        'name',
        'owner',
        'type',
        'voucher'
    ]

    class Meta:
        permissions = ()
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'

    def __str__(self):
        return self.name


class Tax(models.Model):
    description = models.TextField(
        blank=True,
        null=True
    )
    name = models.CharField(
        blank=False,
        max_length=100,
        null=False
    )
    percent = models.FloatField(
        blank=False,
        null=False,
    )

    REQUIRED_FIELDS = [
        'name',
        'percent',
    ]

    class Meta:
        permissions = ()
        verbose_name = 'tax'
        verbose_name_plural = 'taxes'

    def __str__(self):
        return self.name
