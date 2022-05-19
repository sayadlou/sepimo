from modeltranslation.translator import translator, TranslationOptions as BaseTranslationOptions

from .models import *


class TranslationOptions(BaseTranslationOptions):
    fields = (
        'title', 'brand_title', 'brand_description', 'our_mission_text', 'who_we_are_text_1', 'who_we_are_text_2',
        'our_vision_text',)
    required_languages = ('fa', 'en')


class ProfileTranslationOptions(BaseTranslationOptions):
    fields = ('title', 'header_text_big', 'header_text_small',)
    required_languages = ('fa', 'en')


class TitleTranslationOptions(BaseTranslationOptions):
    fields = ('title',)
    required_languages = ('fa', 'en')


translator.register(LoginPage, TitleTranslationOptions)
translator.register(SignUpPage, TitleTranslationOptions)
translator.register(AboutUsPage, TranslationOptions)
translator.register(ProfilePage, ProfileTranslationOptions)
