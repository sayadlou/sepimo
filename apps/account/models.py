from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfileManager(UserManager):
    pass


class UserProfile(AbstractUser):
    objects = UserProfileManager()

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    mobile = models.CharField(_('mobile'), max_length=20, null=True, blank=False)
    phone = models.CharField(_('phone'), max_length=20, null=True, blank=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=False, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=True)
    email = models.EmailField(_('email address'), blank=True)


class Address(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    state = models.CharField(_('state'), max_length=30)
    city = models.CharField(_('city'), max_length=30)
    area = models.CharField(_('area'), max_length=2)
    postal_code = models.CharField(_('city'), max_length=11)
    address = models.TextField(_('address'), max_length=300)
