from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import *


@admin.register(UserProfile)
class MyUserAdmin(UserAdmin):
    pass


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    pass
