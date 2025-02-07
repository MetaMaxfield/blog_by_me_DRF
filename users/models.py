from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from services.users.validator import ImprovedUnicodeUsernameValidator

username_validator = ImprovedUnicodeUsernameValidator()


class User(AbstractUser):
    """Пользователь"""

    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        help_text='Обязательное условие. 150 символов или меньше. Только буквы, цифры, пробелы и @/./+/-/_.',
        validators=[username_validator],
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    description = models.TextField(verbose_name='Информация об пользователе', blank=True)
    image = models.ImageField(verbose_name='Изображение пользователя', upload_to='users/', null=True, blank=True)
    user_rating = models.IntegerField(
        verbose_name='Рейтинг пользователя', default=0, help_text='Общий рейтинг автора, учитывающий лайки и дизлайки'
    )
    is_staff = models.BooleanField(
        verbose_name='Статус персонала',
        default=True,
        help_text='Определяет, может ли пользователь войти ' 'на сайт администрирования.',
    )
    email = models.EmailField(verbose_name="E-mail", blank=False)

    def get_user_groups(self):
        """Метод получения групп пользователя"""
        user_groups = list(self.groups.values_list('name', flat=True))
        if self.is_superuser:
            user_groups.insert(0, _('Администратор'))
        return [_(group_name) for group_name in user_groups]

    get_user_groups.short_description = 'Группы пользователя'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
