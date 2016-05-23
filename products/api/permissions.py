# coding: utf-8

# TASTYPIE
from tastypie.authorization import Authorization


class ProductAuthorization(Authorization):

    def update_list(self, object_list, bundle):
        return False

    def delete_list(self, object_list, bundle):
        return False
