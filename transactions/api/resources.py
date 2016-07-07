# coding: utf-8
from __future__ import unicode_literals

# PYTHON
import ast
import simplejson
import time

# DJANGO
from django.db import IntegrityError, transaction

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie import fields

# INVENTORY
from clients.api.resources import ClientResource
from companies.api.resources import CompanyResource
from products.models import Product
from transactions.models import Transaction
from transactions.api.permissions import TransactionAuthorization

class TransactionResource(ModelResource):

    client = fields.ToOneField(ClientResource, attribute='client', full=True)
    created_at = fields.DateTimeField(readonly=True)
    created_by = fields.IntegerField()
    owner_id = fields.IntegerField()

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        authentication = SessionAuthentication()
        authorization = TransactionAuthorization()
        excludes = ['deleted_at']
        filtering = {
            'type': ('exact')
        }
        queryset = Transaction.objects.all().order_by('-id')
        resource_name = 'transactions'

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_voucher(self, bundle):
        return ast.literal_eval(bundle.obj.voucher)

    def hydrate_voucher(self, bundle):
        bundle.obj.voucher = simplejson.dumps(bundle.data['voucher'])
        return bundle

    def obj_create(self, bundle, **kwargs):
        voucher = bundle.data.get('voucher', {})
        try:
            with transaction.atomic():
                for data in voucher.get('cart', []):
                    product = Product.objects.get(pk=data['id'])

                    if bundle.data['type'] == 'sale':
                        if product.quantity < data['quantity']:
                            raise IntegrityError

                        product.quantity = product.quantity - data['quantity']
                        product.save()
                    elif bundle.data['type'] == 'purchase':
                        product.quantity = product.quantity + data['quantity']
                        product.save()
        except IntegrityError:
            raise BadRequest('No se pudo finalizar la compra. Algún producto no tiene la cantidad suficiente.')

        return super(TransactionResource, self).obj_create(bundle, **kwargs)

    def hydrate_created_by(self, bundle):
        bundle.obj.created_by_id = bundle.request.user.id
        return bundle

    def hydrate_owner_id(self, bundle):
        bundle.obj.owner_id = bundle.request.user.company_id
        return bundle
