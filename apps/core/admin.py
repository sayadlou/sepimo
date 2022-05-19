from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import LoginPage, AboutUsPage, Brand, CustomerReviews, ProfilePage


@admin.register(LoginPage)
class LoginPageAdmin(admin.ModelAdmin):
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


@admin.register(ProfilePage)
class ProfilePageAdmin(TranslationAdmin):
    pass
