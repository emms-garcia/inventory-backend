# coding: utf-8

# PYTHON
import time

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import BadRequest, NotFound
from tastypie import fields

# INVENTORY
from ..models import Product, UOM
from .permissions import ProductAuthorization, UOMAuthorization
from .validations import ProductValidation, UOMValidation
from commons.resources import DatedResource
from users.api.resources import UserResource


class UOMResource(DatedResource):

    id = fields.CharField(attribute='eid', readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        authentication = SessionAuthentication()
        authorization = UOMAuthorization()
        detail_uri_name = 'eid'
        excludes = ['deleted_at', 'eid']
        filtering = {
            'name': ('icontains')
        }
        queryset = UOM.objects.all().order_by('id')
        resource_name = 'uoms'
        validation = UOMValidation()

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime(bundle.obj.updated_at.timetuple())

    def obj_delete(self, bundle, **kwargs):
        bundle.obj = self.obj_get(bundle=bundle, **kwargs)
        if bundle.obj.products.count():
            raise BadRequest('No se puede borrar la unidad de medida. Se encuentra en uso en uno o más productos.')
        else:
            super(UOMResource, self).obj_delete(bundle, **kwargs)

class ProductResource(DatedResource):

    created_at = fields.DateTimeField(readonly=True)
    created_by = fields.ToOneField(UserResource, attribute='created_by')
    id = fields.CharField(attribute='eid', readonly=True)
    uom = fields.ToOneField(UOMResource, attribute='uom', full=True)
    updated_at = fields.DateTimeField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        authentication = SessionAuthentication()
        authorization = ProductAuthorization()
        detail_uri_name = 'eid'
        excludes = ['deleted_at', 'eid']
        queryset = Product.objects.all().order_by('id')
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
        bundle.obj = self.obj_get(bundle=bundle, **kwargs)
        if bundle.obj.group_products.count():
            raise BadRequest('No se puede borrar el producto. Se encuentra en uso en uno o más grupos.')
        else:
            super(ProductResource, self).obj_delete(bundle, **kwargs)
