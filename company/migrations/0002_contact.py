# Generated by Django 4.2.1 on 2024-11-06 11:42

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Эл. почта')),
                (
                    'phone',
                    phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон'),
                ),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('feedback', models.BooleanField(default=False, verbose_name='Обрантая связь')),
            ],
            options={
                'verbose_name': 'Запрос от пользователя блога',
                'verbose_name_plural': 'Запросы от пользователей блога',
            },
        ),
    ]