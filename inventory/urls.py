from django.conf.urls import include, url
from django.contrib import admin

from tastypie.api import Api

from accounts.api.resources import AccountResource
from clients.api.resources import ClientResource

api = Api(api_name='inventory')
api.register(AccountResource())
api.register(ClientResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
]
