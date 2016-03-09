# coding: utf-8

# PYTHON
import time

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource
from tastypie import fields

# INVENTORY
from ..models import Client
from .permissions import ClientAuthorization
from .validations import ClientValidation
from users.api.resources import UserResource


class ClientResource(ModelResource):

    created_at = fields.DateTimeField(readonly=True)
    created_by = fields.ToOneField(UserResource, attribute='created_by')
    updated_at = fields.DateTimeField(readonly=True)

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

    def hydrate_created_by(self, bundle):
        bundle.obj.created_by = bundle.request.user
        return bundle
