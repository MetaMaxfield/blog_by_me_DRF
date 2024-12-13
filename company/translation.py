from modeltranslation.translator import TranslationOptions, register

from .models import About


@register(About)
class AboutTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('description',)
