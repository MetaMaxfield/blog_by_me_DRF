from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class Category(models.Model):
    """Котегории"""

    name = models.CharField(verbose_name='Категория', max_length=150)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Video(models.Model):
    """Видео"""

    title = models.CharField(max_length=100, verbose_name='Заголовок видео')
    description = models.TextField(verbose_name='Описание видео')
    file = models.FileField(
        upload_to='video/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name='Видеофайл'
    )
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-create_at',)
        verbose_name = 'Видеозапись'
        verbose_name_plural = 'Видеозаписи'


class Post(models.Model):
    """Пост"""

    title = models.CharField(verbose_name='Заголовок', max_length=250)
    url = models.SlugField(max_length=25, unique_for_date='publish', unique=True)
    author = models.ForeignKey(
        'users.User', verbose_name='Автор', on_delete=models.CASCADE, related_name='post_author', null=True
    )
    category = models.ForeignKey(
        'blog.Category', verbose_name='Категория', related_name='post_category', on_delete=models.SET_NULL, null=True
    )
    tags = TaggableManager(related_name='post_tags')
    body = models.TextField(verbose_name='Содержание')
    video = models.OneToOneField(
        Video,
        verbose_name='Видео к записи',
        related_name='post_video',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    image = models.ImageField(verbose_name='Изображение', upload_to='posts/')
    publish = models.DateTimeField(
        default=timezone.now,
        help_text='Укажите дату и время, когда пост должен быть опубликован. '
        'Оставьте текущую дату и время для немедленной публикации, '
        'либо выберите будущую дату для отложенного поста. '
        'Обратите внимание: изменить время публикации можно будет только '
        'до наступления ранее указанного времени.',
        verbose_name='Время публикации',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False, verbose_name='Черновик')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        indexes = [
            models.Index(fields=('-publish', '-id'), name='publish_id_idx'),
        ]
        ordering = ('-publish', '-id')


class Comment(models.Model):
    """Комментарии"""

    post = models.ForeignKey('blog.Post', verbose_name='Запись', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
    )
    name = models.CharField(verbose_name='Имя', max_length=80)
    email = models.EmailField()
    text = models.TextField(verbose_name='Содержание комментария', max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Комментарий от {self.name} к {self.post}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)


class Mark(models.Model):
    """Оценка"""

    nomination = models.CharField(verbose_name='Наименование', max_length=10)
    value = models.SmallIntegerField(verbose_name="Значение", default=0)

    def __str__(self):
        return self.nomination

    class Meta:
        verbose_name = 'Значение рейтинга'
        verbose_name_plural = 'Значения рейтинга'
        ordering = ('value',)


class Rating(models.Model):
    """Рейтинг"""

    ip = models.CharField(verbose_name='IP адрес', max_length=15)
    mark = models.ForeignKey('blog.Mark', verbose_name='Оценка', on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', verbose_name='Пост', on_delete=models.CASCADE, related_name='rating_post')

    def __str__(self):
        return f'{self.mark}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
