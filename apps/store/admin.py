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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class ProductAdmin(admin.ModelAdmin):
    pass
