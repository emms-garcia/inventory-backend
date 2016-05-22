# coding: utf-8

# PYTHON
import time

# DJANGO
from django.conf.urls import url

# TASTYPIE
from tastypie import fields
from tastypie.resources import ModelResource


class DatedResource(ModelResource):
    created_at = fields.DateTimeField(readonly=True)
    updated_at = fields.DateTimeField(readonly=True)

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime
