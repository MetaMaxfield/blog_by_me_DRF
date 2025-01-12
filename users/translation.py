from modeltranslation.translator import TranslationOptions, register

from .models import User


@register(User)
class UserTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('description',)
