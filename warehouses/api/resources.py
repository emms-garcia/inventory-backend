# coding: utf-8
from __future__ import unicode_literals

# TASTYPIE
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

# INVENTORY
from products.api.resources import ProductResource
from warehouses.models import Warehouse, WarehouseStock
from warehouses.api.permissions import WarehouseAuthorization


class WarehouseResource(ModelResource):

    class Meta:
        allowed_methods = ['get', 'patch', 'delete']
        authentication = SessionAuthentication()
        authorization = WarehouseAuthorization()
        excludes = ['deleted_at']
        queryset = Warehouse.objects.all().order_by('-id')
        resource_name = 'warehouses'

    def obj_delete(self, bundle, **kwargs):
        if bundle.obj.owner.warehouses.count() == 1:
            raise BadRequest('No se pueden borrar todos los almacenes.')
        return super(WarehouseResource, self).obj_delete(bundle, **kwargs)


class WarehouseStockResource(ModelResource):

    product = fields.ToOneField(
        ProductResource, attribute='product', full=True)
    warehouse = fields.ToOneField(
        WarehouseResource, attribute='warehouse', full=True)

    class Meta:
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        excludes = []
        filtering = {
            'product': ('exact')
        }
        queryset = WarehouseStock.objects.all().order_by('-id')
        resource_name = 'warehouse_stocks'
