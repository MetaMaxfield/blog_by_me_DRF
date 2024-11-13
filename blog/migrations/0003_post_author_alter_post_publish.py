# Generated by Django 4.2.1 on 2024-11-10 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_alter_post_options_alter_comment_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='post_author',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Автор',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text='Укажите дату и время, когда пост должен быть опубликован. Оставьте текущую дату и время для немедленной публикации, либо выберите будущую дату для отложенного поста. Обратите внимание: изменить время публикации можно будет только до наступления ранее указанного времени.',
                verbose_name='Время публикации',
            ),
        ),
    ]