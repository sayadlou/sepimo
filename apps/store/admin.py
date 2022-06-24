from django.contrib import admin

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
class ProductAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('core/css/admin_product.css',)
        }
        js = ('core/js/admin_product.js',)

    prepopulated_fields = {'slug': ('title',)}
    exclude = ('code','slug')
    inlines = [VariantInLine]


@admin.register(Payment)
class ProductAdmin(admin.ModelAdmin):
    pass
