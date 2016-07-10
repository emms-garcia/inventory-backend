# coding: utf-8
from __future__ import unicode_literals

# TASTYPIE
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource

# INVENTORY
from uoms.api.permissions import UOMAuthorization
from uoms.models import UOM


class UOMResource(ModelResource):

    owner_id = fields.IntegerField()

    class Meta:
        allowed_methods = ['get', 'post', 'patch', 'delete']
        authentication = SessionAuthentication()
        authorization = UOMAuthorization()
        excludes = ['deleted_at']
        queryset = UOM.objects.all().order_by('-id')
        resource_name = 'uoms'

    def hydrate_owner_id(self, bundle):
        bundle.obj.owner_id = bundle.request.user.company_id
        return bundle
