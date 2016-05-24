# coding: utf-8

# DJANGO
from django.db import models
from django.utils import timezone

# INVENTORY
from commons.utils import get_uuid


class Address(models.Model):
    address = models.CharField(
        blank=True,
        max_length=254,
        null=True)
    city = models.CharField(
        blank=True,
        max_length=100,
        null=True)
    state = models.CharField(
        blank=True,
        max_length=100,
        null=True)
    country = models.CharField(
        blank=True,
        max_length=100,
        null=True)
    code = models.CharField(
        blank=True,
        max_length=32,
        null=True)

    class Meta:
        abstract = True


class EID(models.Model):
    eid = models.CharField(
        blank=False,
        default=get_uuid,
        max_length=32,
        null=False)

    class Meta:
        abstract = True


class Dated(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True)
    updated_at = models.DateTimeField(
        null=True)
    deleted_at = models.DateTimeField(
        null=True)

    class Meta:
        abstract = True

    def create(self, *args, **kwargs):
        super(Dated, self).create(*args, **kwargs)
        self.updated_at = self.created_at

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Dated, self).save(*args, **kwargs)
