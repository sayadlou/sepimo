from modeltranslation.translator import translator, TranslationOptions as BaseTranslationOptions

from .models import *


class PostTranslationOptions(BaseTranslationOptions):
    fields = ('title', 'intro', 'content', 'content2',)
    required_languages = ('fa', 'en')


class CategoryTranslationOptions(BaseTranslationOptions):
    fields = ('name', 'slug')
    required_languages = ('fa', 'en')


translator.register(Post, PostTranslationOptions)
# translator.register(Category, CategoryTranslationOptions)
