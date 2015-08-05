# coding: utf-8

# DJANGO
from django.contrib import admin

# INVENTORY
from clients.models import Client


class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, AuthorAdmin)
