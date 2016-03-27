# coding: utf-8

# DJANGO
from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=254, null=False, blank=True)
    phone = models.CharField(max_length=20, null=False, blank=True)
    rfc = models.CharField(max_length=100, null=False, blank=True)

    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name
