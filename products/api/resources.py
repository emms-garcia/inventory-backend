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
from ..models import Product
from .permissions import ProductAuthorization
from .validations import ProductValidation
from commons.resources import DatedResource
from users.api.resources import UserResource


class ProductResource(DatedResource):

    created_at = fields.DateTimeField(readonly=True)
    created_by = fields.ToOneField(UserResource, attribute='created_by')
    id = fields.CharField(attribute='eid', readonly=True)
    updated_at = fields.DateTimeField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        authentication = SessionAuthentication()
        authorization = ProductAuthorization()
        detail_uri_name = 'eid'
        excludes = ['deleted_at', 'eid']
        queryset = Product.objects.all().order_by('-id')
        resource_name = 'products'
        validation = ProductValidation()

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime(bundle.obj.updated_at.timetuple())

    def hydrate_created_by(self, bundle):
        bundle.obj.created_by = bundle.request.user
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
                        'created_by': request.user,
                        'name': row[0],
                        'description': row[1],
                        'price_per_unit': row[2],
                        'quantity': row[3]
                    }
                    Product.objects.create(**params)
        except Exception:
            return HttpBadRequest('Archivo invalido')

        return HttpResponse()
