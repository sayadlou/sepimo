from django.contrib import admin

from .models import LoginPage, AboutUsPage, Brand, CustomerReviews


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
class AboutUsPageAdmin(admin.ModelAdmin):
    pass
