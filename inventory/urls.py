# coding: utf-8

# DJANGO
from django.conf.urls import include, url
from django.contrib import admin

# TASTYPIE
from tastypie.api import Api

# INVENTORY
from clients.api.resources import ClientResource
from products.api.resources import ProductResource, UOMResource
from users.api.resources import UserResource


api = Api(api_name='inventory')
api.register(ClientResource())
api.register(ProductResource())
api.register(UOMResource())
api.register(UserResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
]
