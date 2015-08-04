
# DJANGO
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# INVENTORY
from utils.models import Dated

# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self, username, password, first_name, last_name, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, password=password, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, first_name, last_name, **extra_fields)

    def create_superuser(self, username, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self._create_user(username, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, Dated, PermissionsMixin):
    
    first_name = models.CharField(max_length=254, null=False, blank=True)
    last_name = models.CharField(max_length=254, null=False, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        permissions = (
        )
        verbose_name = "user"
        verbose_name_plural = "users"
   
    def __str__(self):
        return self.username

    def get_full_name():
        return self.first_name + ' ' + self.last_name

    def get_short_name():
        return self.first_name


