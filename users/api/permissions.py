# coding: utf-8
from __future__ import unicode_literals

"""
    Permissions for Account Resource.
"""

# DJANGO
from django.db.models import Q

# TASTYPIE
from tastypie.authorization import Authorization


class UserAuthorization(Authorization):

    def create_list(self, object_list, bundle):
        return bundle.request.user.is_superuser

    def read_list(self, object_list, bundle):
        if bundle.request.user.parent == None:
            return object_list.filter(Q(parent=bundle.request.user) | Q(id=bundle.request.user.id))
        else:
            return object_list.filter(id=bundle.request.user.id)

    def read_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user or \
            bundle.request.user.parent == None or \
            bundle.request.is_superuser

    def update_list(self, object_list, bundle):
        return False

    def update_detail(self, object_list, bundle):
        return bundle.obj.id == bundle.request.user.id or \
            bundle.request.user.parent == None or \
            bundle.request.user.is_superuser

    def delete_list(self, object_list, bundle):
        return False

    def delete_detail(self, object_list, bundle):
        return bundle.request.user.is_superuser \
            and not (bundle.request.user.id == bundle.obj.id)
