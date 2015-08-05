# coding: utf-8

# DJANGO
from django.db import models

# INVENTORY
from utils.models import Dated


class Client(Dated):

    name = models.CharField(max_length=100, null=False, blank=True)
    email = models.EmailField(max_length=254)
    company = models.CharField(max_length=100, null=False, blank=True)
    rfc = models.CharField(max_length=100, null=False, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=True)
    cellphone = models.CharField(max_length=20, null=False, blank=True)
    address = models.CharField(max_length=254, null=False, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    REQUIRED_FIELDS = ['name', 'company']

    class Meta:
        permissions = ()
        verbose_name = "client"
        verbose_name_plural = "clients"
   
    def __str__(self):
        return self.name
