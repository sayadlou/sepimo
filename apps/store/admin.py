from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import DraggableMPTTAdmin

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


class ImageInline(admin.StackedInline):
    model = Image
    min_num = 1
    max_num = 4
    extra = 0


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    # class Media:
    #     css = {
    #         'all': ('core/css/admin_product.css',)
    #     }
    #     js = ('core/js/admin_product.js',)

    exclude = ('code',)
    inlines = [ImageInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
