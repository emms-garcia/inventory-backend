# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.db import models

# INVENTORY
from commons.models import Dated


class Client(Dated):


    address = models.CharField(max_length=254, null=False, blank=True)
    cellphone = models.CharField(max_length=20, null=False, blank=True)
    company = models.CharField(max_length=100, null=False, blank=True)
    created_by = models.ForeignKey('users.User', related_name='clients')
    email = models.EmailField(max_length=254)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=True)
    rfc = models.CharField(max_length=100, null=False, blank=True)

    REQUIRED_FIELDS = ['name', 'company', 'owner']

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return self.name
