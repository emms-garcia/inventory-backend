# coding: utf-8

# PYTHON
import time

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie import fields

# INVENTORY
from ..models import GroupProduct, ProductGroup
from commons.resources import DatedResource
from products.api.resources import ProductResource
from users.api.resources import UserResource


class GroupProductResource(DatedResource):

    class Meta:
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        detail_uri_name = 'eid'
        excludes = ['deleted_at']
        queryset = GroupProduct.objects.all().order_by('-id')
        resource_name = 'group_products'


class ProductGroupResource(DatedResource):

    created_by = fields.ToOneField(UserResource, attribute='created_by')
    id = fields.CharField(attribute='eid', readonly=True)
    total = fields.FloatField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        authorization = Authorization()
        authentication = SessionAuthentication()
        detail_uri_name = 'eid'
        excludes = ['deleted_at', 'eid']
        queryset = ProductGroup.objects.all().order_by('id')
        resource_name = 'product_groups'

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_total(self, bundle):
        group_products = GroupProduct.objects.filter(group=bundle.obj)
        return sum([gp.product.price_per_unit * gp.quantity for gp in group_products])

    def dehydrate_updated_at(self, bundle):
        if bundle.obj.updated_at:
            return time.mktime(bundle.obj.updated_at.timetuple())

    def hydrate_created_by(self, bundle):
        bundle.obj.created_by = bundle.request.user
        return bundle

    def obj_create(self, bundle, **kwargs):
        products = bundle.data.get('products', [])
        bundle = super(ProductGroupResource, self).obj_create(bundle, **kwargs)
        for product in products:
            product_uri, product_quantity = product.get('resource_uri'), product.get('quantity')
            product_obj = ProductResource().get_via_uri(product_uri, bundle.request)
            GroupProduct.objects.create(
                group=bundle.obj,
                product=product_obj,
                quantity=int(product_quantity))
        return bundle
