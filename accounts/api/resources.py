# -*- coding: utf-8 -*-

# PYTHON
from datetime import datetime
import time

# DJANGO
from django.conf.urls import url
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpAccepted, HttpBadRequest, HttpNotFound, HttpResponse, HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.validation import CleanedDataFormValidation
from tastypie import fields

# INVENTORY
from accounts.forms import UserForm
from accounts.models import User

class AccountResource(ModelResource):

    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()
    permissions = fields.CharField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = Authorization()
        excludes = ['password', 'deleted_at', 'updated_at']
        queryset = User.objects.all()
        resource_name = 'account'
        validation = CleanedDataFormValidation(form_class=UserForm)

    def post_list(self, request, **kwargs):
        print request.body
        return HttpBadRequest()
        return super(AccountResource, self).post_list(request, **kwargs)

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_last_login(self, bundle):
        if bundle.obj.last_login:
            return time.mktime(bundle.obj.last_login.timetuple())

    def dehydrate_permissions(self, bundle):
        permissions = 'R'
        if bundle.data.get('is_superuser'):
            permissions = 'RWD'
        elif bundle.data.get('is_staff') and not bundle.data.get('is_superuser'): 
            permissions = 'RW'
        return permissions

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/login%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
            url(r'^(?P<resource_name>%s)/(?P<pk>\d+)/change_password%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('change_password'), name='api_change_password'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                bundle = self.build_bundle(obj=user, request=request)
                desired_format = self.determine_format(request)
                data = self.serialize(request, self.full_dehydrate(bundle), desired_format)
                return HttpResponse(data)
            else:
                return HttpUnauthorized()
        else:
            return HttpUnauthorized()

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        logged_out = auth_logout(request)
        return HttpAccepted()

    def change_password(self, request, **kwargs):
        self.method_check(request, allowed=['patch'])
        self.is_authenticated(request)

        try:
            user_to_update = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return HttpNotFound()
    
        if user_to_update.id == request.user.id or request.user.is_superuser:
            data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
            password = data.get('password')
            if password:
                user_to_update.set_password(password)
                user_to_update.save()
                if user_to_update.id == request.user.id:
                    user = authenticate(username=user_to_update.username, password=password)
                    auth_login(request, user)
                return HttpAccepted()
            else:
                return HttpBadRequest()
        else:
            return HttpUnauthorized()
