from django.contrib import admin
from django.contrib.admin import ModelAdmin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import Post, Category, Comment, PostViewHistory


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    search_fields = ['title', 'slug']
    list_display = ['title', 'slug']
    # readonly_fields = ['id']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class PostAdmin(ModelAdmin):
    pass


@admin.register(PostViewHistory)
class PostAdmin(ModelAdmin):
    pass
