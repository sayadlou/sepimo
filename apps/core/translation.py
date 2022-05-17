from modeltranslation.translator import translator, TranslationOptions as BaseTranslationOptions

from .models import AboutUsPage


class TranslationOptions(BaseTranslationOptions):
    fields = (
        'title', 'brand_title', 'brand_description', 'our_mission_text', 'who_we_are_text_1', 'who_we_are_text_2',
        'our_vision_text',)
    required_languages = ('fa', 'en')


translator.register(AboutUsPage, TranslationOptions)
