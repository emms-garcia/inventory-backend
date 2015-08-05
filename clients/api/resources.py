# coding: utf-8

# PYTHON
from datetime import datetime
import time

# DJANGO
from django.conf.urls import url

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.http import HttpAccepted, HttpResponse, HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields

# INVENTORY
from clients.models import Client
from permissions import ClientAuthorization
from validations import ClientValidation

class ClientResource(ModelResource):

    created_at = fields.DateTimeField(readonly=True)
    updated_at = fields.DateTimeField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = ClientAuthorization()
        excludes = ['deleted_at']
        queryset = Client.objects.all().order_by('id')
        resource_name = 'client'
        validation = ClientValidation()

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime(bundle.obj.updated_at.timetuple())
