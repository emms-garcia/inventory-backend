# coding: utf-8
from __future__ import unicode_literals

# TASTYPIE
from tastypie.authorization import Authorization


class ClientAuthorization(Authorization):

    def create_list(self, object_list, bundle):
        return bundle.request.user.is_superuser or bundle.request.user.is_staff

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        return []

    def update_detail(self, object_list, bundle):
        return bundle.request.user.is_superuser or bundle.request.user.is_staff

    def delete_list(self, object_list, bundle):
        return []

    def delete_detail(self, object_list, bundle):
        return bundle.request.user.is_superuser or bundle.request.user.is_staff
