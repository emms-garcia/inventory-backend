# coding: utf-8

# DJANGO
from django.db import models
from django.utils import timezone

# INVENTORY
from commons.utils import get_uuid


class EID(models.Model):
    eid = models.CharField(
        blank=False,
        default=get_uuid,
        max_length=32,
        null=False)

    class Meta:
        abstract = True


class Dated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def create(self, *args, **kwargs):
        super(Dated, self).create(*args, **kwargs)
        self.updated_at = self.created_at

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Dated, self).save(*args, **kwargs)
