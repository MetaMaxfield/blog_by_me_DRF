import re

from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError


def validate_date_format(date: str) -> None:
    """Проверяет формат даты (YYYY-MM-DD)"""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        raise ValidationError({'detail': _('Задан неправильный формат даты')})


def validate_q_param(q: str) -> None:
    """Проверяет, что параметр поиска не пустой"""
    if not q:
        raise ValidationError({'detail': _('Пожалуйста, введите текст для поиска постов.')})
