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
    email = models.EmailField(_('email address'), blank=True, unique=True)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    province = models.CharField(_('Province'), max_length=30)
    city = models.CharField(_('City'), max_length=30)
    phone_number = models.CharField(_('Phone Number'), max_length=30)
    area = models.CharField(_('area'), max_length=2)
    postal_code = models.CharField(_('Postal Code'), max_length=11)
    address = models.TextField(_('Address'), max_length=300)

    def __str__(self):
        return f"{self.owner.username} {self.address}"
