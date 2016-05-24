# coding: utf-8
from __future__ import unicode_literals

# TASTYPIE
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource

# INVENTORY
from products.api.resources import ProductResource
from warehouses.models import Warehouse, WarehouseStock


class WarehouseResource(ModelResource):

    class Meta:
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        excludes = ['deleted_at']
        queryset = Warehouse.objects.all().order_by('-id')
        resource_name = 'warehouses'


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
