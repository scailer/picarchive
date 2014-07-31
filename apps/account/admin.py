# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
    list_display = ['username', 'email']

admin.site.register(models.User, UserAdmin)
