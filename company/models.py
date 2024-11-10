from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class About(models.Model):
    """Информация о компании"""

    description = models.TextField(verbose_name='Основная информация о компании', null=True, blank=True)
    email_contact = models.EmailField(verbose_name='Эл. почта для контакта', null=True, blank=True)
    phone1_num = PhoneNumberField(verbose_name='Мобильный телефон', null=True, blank=True)
    phone2_num = PhoneNumberField(verbose_name='Стационарный телефон', null=True, blank=True)
    address = models.CharField(verbose_name='Адрес компании', null=True, blank=True)
    latitude = models.DecimalField(
        verbose_name='Координата широты', max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        verbose_name='Координата долготы', max_digits=9, decimal_places=6, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            raise ValidationError('Нельзя создать более одного экземпляра модели About.')
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Страница "О нас" с контактной информацией'

    class Meta:
        verbose_name = 'Содержание страницы "О нас"'
        verbose_name_plural = 'Содержание страницы "О нас"'


class Contact(models.Model):
    """Обратная связь"""

    name = models.CharField(verbose_name='Имя')
    email = models.EmailField(verbose_name='Эл. почта')
    phone = PhoneNumberField(verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(auto_now_add=True)
    feedback = models.BooleanField(verbose_name='Обрантая связь', default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Запрос от пользователя блога'
        verbose_name_plural = 'Запросы от пользователей блога'
