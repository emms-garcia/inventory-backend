# coding: utf-8
from __future__ import unicode_literals

# DJANGO
from django.conf.urls import include, url
from django.contrib import admin

# TASTYPIE
from tastypie.api import Api

# INVENTORY
from clients.api.resources import ClientResource
from products.api.resources import ProductResource
from product_groups.api.resources import GroupProductResource, ProductGroupResource
from users.api.resources import UserResource
from warehouses.api.resources import WarehouseResource, WarehouseStockResource


api = Api(api_name='inventory')
api.register(ClientResource())
api.register(GroupProductResource())
api.register(ProductResource())
api.register(ProductGroupResource())
api.register(UserResource())
api.register(WarehouseResource())
api.register(WarehouseStockResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
]
