from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm as UserCreationFormOrg
from django.utils.translation import gettext_lazy as _

from .models import *


class UserCreationForm(UserCreationFormOrg):
    class Meta:
        fields = ("username", "email")


@admin.register(UserProfile)
class MyUserAdmin(UserAdmin):
    # add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    pass
