# coding: utf-8
from __future__ import unicode_literals

# TASTYPIE
from tastypie.authorization import Authorization


class ProductAuthorization(Authorization):

    def update_list(self, object_list, bundle):
        return False

    def delete_list(self, object_list, bundle):
        return False
