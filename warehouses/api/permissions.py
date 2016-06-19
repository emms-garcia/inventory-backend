# coding: utf-8
from __future__ import unicode_literals

# TASTYPIE
from tastypie.authorization import Authorization


class WarehouseAuthorization(Authorization):

    def delete_detail(self, object_list, bundle):
      return bundle.obj.owner_id == bundle.request.user.company_id

    def update_list(self, object_list, bundle):
        return False

    def delete_list(self, object_list, bundle):
        return False
