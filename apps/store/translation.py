from modeltranslation.translator import translator, TranslationOptions as BaseTranslationOptions

from .models import *


class ProductTranslationOptions(BaseTranslationOptions):
    fields = ('title', 'slug', 'description', 'variant_title',)
    required_languages = {'default': ('title', 'slug', 'description',)}


translator.register(Product, ProductTranslationOptions)
