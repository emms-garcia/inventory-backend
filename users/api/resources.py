# coding: utf-8

# PYTHON
import time

# DJANGO
from django.conf.urls import url
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError

# TASTYPIE
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import BadRequest
from tastypie.http import HttpAccepted, HttpBadRequest, HttpCreated, HttpResponse, HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields

# INVENTORY
from ..models import User, UserManager
from .permissions import UserAuthorization
from .validations import UserValidation


class UserResource(ModelResource):

    created_at = fields.FloatField(readonly=True)
    last_login = fields.FloatField(readonly=True)

    class Meta:
        allowed_methods = ['get', 'patch', 'post', 'delete']
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        excludes = ['password', 'deleted_at', 'updated_at']
        queryset = User.objects.all()
        resource_name = 'users'
        validation = UserValidation()

    def dehydrate_created_at(self, bundle):
        if bundle.obj.created_at:
            return time.mktime(bundle.obj.created_at.timetuple())

    def dehydrate_last_login(self, bundle):
        if bundle.obj.last_login:
            return time.mktime(bundle.obj.last_login.timetuple())

    def obj_update(self, bundle, **kwargs):
        bundle = super(UserResource, self).obj_update(bundle, **kwargs)
        if bundle.data.has_key('password'):
            bundle.obj.set_password(bundle.data['password'])
            bundle.obj.save()
            user = authenticate(
                username=bundle.obj.username, password=bundle.data['password'])
            auth_login(bundle.request, user)
        return bundle

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/signup%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name='api_signup'),
            url(r'^(?P<resource_name>%s)/login%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout')
        ]

    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))

        data['is_staff'] = True
        username = data.pop('username')

        try:
            User.objects.create_user(username, **data)
            return HttpCreated()
        except IntegrityError:
            return HttpBadRequest('Este nombre de usuario ya fue utilizado.')
        except Exception:
            return HttpBadRequest()

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                bundle = self.build_bundle(obj=user, request=request)
                desired_format = self.determine_format(request)
                data = self.serialize(
                    request, self.full_dehydrate(bundle), desired_format)
                return HttpResponse(data)
            else:
                return HttpUnauthorized()
        else:
            return HttpUnauthorized()

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        logged_out = auth_logout(request)
        return HttpAccepted()