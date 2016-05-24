# coding: utf-8

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource

# INVENTORY
from companies.models import Company


class CompanyResource(ModelResource):

    class Meta:
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        excludes = ['deleted_at']
        queryset = Company.objects.all().order_by('-id')
        resource_name = 'companies'
