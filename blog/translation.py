from modeltranslation.translator import TranslationOptions, register

from .models import Category, Mark, Post, Video


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('name', 'description')


@register(Video)
class VideoTranslationsOption(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('title', 'description')


@register(Post)
class PostTranslationsOption(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('title', 'body')


@register(Mark)
class MarkTranslationsOption(TranslationOptions):
    """Мультиязычность выбранных полей"""

    fields = ('nomination',)
