# -*- coding: utf-8 -*-

# TASTYPIE
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class AccountAuthorization(Authorization):

    def create_list(self, object_list, bundle):
        return bundle.request.user.is_superuser

    def read_list(self, object_list, bundle):
        if bundle.request.user.is_superuser:
            return object_list.order_by('first_name')
        else:
            return object_list.filter(pk=bundle.request.user.id)

    def read_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user or bundle.request.user.is_superuser

    def update_list(self, object_list, bundle):
        return False

    def update_detail(self, object_list, bundle):
        return bundle.obj.id == bundle.request.user.id or bundle.request.user.is_superuser

    def delete_list(self, object_list, bundle):
        return False

    def delete_detail(self, object_list, bundle):
        return bundle.request.user.is_superuser and \
            not bundle.obj.is_superuser and \
            not (bundle.request.user.id == bundle.obj.id)
