# coding: utf-8

# DJANGO
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

# INVENTORY
from commons.models import Dated, EID
from companies.models import Company


class UserManager(BaseUserManager):

    def _create_user(self, username, password, first_name, last_name, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        username = self.normalize_email(username)
        user = self.model(username=username, password=password,
                          first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _get_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            group = None
        return group

    def create_account(self, username, password=None, first_name=None, last_name=None, **extra_fields):
        extra_fields['company'] = Company.objects.create(name=extra_fields.get('company'))
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(username, password, first_name, last_name, **extra_fields)
        group = self._get_group('accounts')
        if group:
            user.groups.add(group)
        return user

    def create_user(self, username, password=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(username, password, first_name, last_name, **extra_fields)
        group = self._get_group('users')
        if group:
            user.groups.add(group)
        return user

    def create_superuser(self, username, password=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        user = self._create_user(username, password, first_name, last_name, **extra_fields)
        group = self._get_group('admins')
        if group:
            user.groups.add(group)
        return user


class User(AbstractBaseUser, Dated, EID, PermissionsMixin):

    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.EmailField(max_length=254, unique=True)

    parent = models.ForeignKey('self', null=True, blank=True)

    company = models.ForeignKey('companies.Company',
        related_name='users', null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def get_permissions(self):
        return list(self.get_all_permissions())

    def get_parent(self):
        return self.parent if self.parent else self
