from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import AboutUsPage, Brand, CustomerReviews, ProfilePage, SignPage, PasswordResetPage


@admin.register(SignPage)
class SignPageAdmin(TranslationAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerReviews)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutUsPage)
class AboutUsPageAdmin(TranslationAdmin):
    pass


@admin.register(PasswordResetPage)
class PasswordResetAdmin(TranslationAdmin):
    pass


@admin.register(ProfilePage)
class ProfilePageAdmin(TranslationAdmin):
    pass
