from modeltranslation.translator import translator, TranslationOptions as BaseTranslationOptions

from .models import *


class ProductTranslationOptions(BaseTranslationOptions):
    fields = ('title', 'slug', 'description', 'intro', 'variant_title', 'more_info', 'send_and_return')
    required_languages = {'default': ('title', 'slug', 'description', 'intro', 'more_info', 'send_and_return')}


translator.register(Product, ProductTranslationOptions)
