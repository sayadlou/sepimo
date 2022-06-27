from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


class CartItemInLine(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner']
    readonly_fields = ['id']
    inlines = [CartItemInLine]


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['owner']
    list_display = ['owner', ]
    readonly_fields = ['id']
    inlines = [OrderItemInLine]


class VariantInLine(admin.TabularInline):
    model = Variant
    fields = ('price', 'differentiation_value')


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    class Media:
        css = {
            'all': ('core/css/admin_product.css',)
        }
        js = ('core/js/admin_product.js',)

    exclude = ('code',)
    inlines = [VariantInLine]


@admin.register(Payment)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
