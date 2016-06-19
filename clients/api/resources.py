# coding: utf-8
from __future__ import unicode_literals

# PYTHON
import time

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource
from tastypie import fields

# INVENTORY
from clients.models import Client
from clients.api.permissions import ClientAuthorization
from clients.api.validations import ClientValidation
from companies.api.resources import CompanyResource


class ClientResource(ModelResource):

    created_at = fields.DateTimeField(readonly=True)
    updated_at = fields.DateTimeField(readonly=True)
    owner_id = fields.IntegerField()

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = ClientAuthorization()
        excludes = ['deleted_at']
        queryset = Client.objects.all().order_by('id')
        resource_name = 'clients'
        validation = ClientValidation()

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime(bundle.obj.updated_at.timetuple())

    def obj_create(self, bundle, **kwargs):
        return super(ClientResource, self).obj_create(bundle, **kwargs)

    def hydrate_owner_id(self, bundle):
        bundle.obj.owner_id = bundle.request.user.company_id
        return bundle
