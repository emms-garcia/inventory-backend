# coding: utf-8

# PYTHON
import csv
import time

# DJANGO
from django.conf.urls import url

# TASTYPIE
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import BadRequest, NotFound
from tastypie.http import HttpBadRequest, HttpResponse
from tastypie.utils import trailing_slash

# INVENTORY
from commons.resources import DatedResource
from companies.api.resources import CompanyResource
from products.models import Product
from products.api.permissions import ProductAuthorization
from products.api.validations import ProductValidation


class ProductResource(DatedResource):

    created_at = fields.DateTimeField(readonly=True)
    owner = fields.ToOneField(CompanyResource, attribute='owner')
    quantity = fields.FloatField(readonly=True)
    updated_at = fields.DateTimeField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        authentication = SessionAuthentication()
        authorization = ProductAuthorization()
        excludes = ['deleted_at']
        queryset = Product.objects.all().order_by('-id')
        resource_name = 'products'
        validation = ProductValidation()

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime(bundle.obj.updated_at.timetuple())

    def dehydrate_quantity(self, bundle):
        return sum([stock.quantity for stock in bundle.obj.stock.all()])

    def hydrate_owner(self, bundle):
        bundle.obj.owner = bundle.request.user.company
        return bundle

    def obj_delete(self, bundle, **kwargs):
        if bundle.obj.group_products.count():
            raise BadRequest('No se puede borrar el producto "{}".'
                'Se encuentra en uso en uno o más grupos.'.format(bundle.obj.name))
        else:
            super(ProductResource, self).obj_delete(bundle, **kwargs)

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/import%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('import_products'), name='api_import_products'),
        ]

    def import_products(self, request, **kwargs):
        self.is_authenticated(request)
        self.method_check(request, allowed=['post'])

        if not request.FILES.get('file'):
            return HttpBadRequest('No se especifico ningún archivo.')

        try:
            with request.FILES['file'] as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in csv_reader:
                    params = {
                        'owner_id': request.user.company_id,
                        'name': row[0],
                        'description': row[1],
                        'price': row[2]
                    }
                    Product.objects.create(**params)
        except Exception as e:
            return HttpBadRequest('Archivo invalido')

        return HttpResponse()
