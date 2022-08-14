from modeltranslation.translator import translator, TranslationOptions as BaseTranslationOptions

from .models import *


class TranslationOptions(BaseTranslationOptions):
    fields = ('title', 'brand_title', 'brand_description', 'our_mission_text', 'who_we_are_text_1', 'who_we_are_text_2',
              'our_vision_text',)
    required_languages = ('fa', 'en')


class ProfileTranslationOptions(BaseTranslationOptions):
    fields = ('title', 'header_text_big', 'header_text_small', 'menu_dashboard', 'menu_orders', 'menu_address',
              'menu_profile', 'menu_logout', 'menu_password_change')
    required_languages = ('fa', 'en')


class BlogPageTranslationOptions(BaseTranslationOptions):
    fields = ('title',)
    required_languages = ('fa', 'en')


class TitleTranslationOptions(BaseTranslationOptions):
    fields = ('title',)
    required_languages = ('fa', 'en')


class PasswordResetOptions(BaseTranslationOptions):
    fields = ('title', 'text_head', 'text_help', 'password_sent_message')
    required_languages = ('fa', 'en')


translator.register(SignPage, TitleTranslationOptions)
translator.register(HomePage, TitleTranslationOptions)
translator.register(PasswordResetPage, PasswordResetOptions)
translator.register(AboutUsPage, TranslationOptions)
translator.register(ProfilePage, ProfileTranslationOptions)
translator.register(BlogPage, BlogPageTranslationOptions)
