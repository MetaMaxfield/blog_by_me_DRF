from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from taggit.models import Tag

from blog.models import Category, Comment, Post, Rating, Video
from blog_by_me_DRF.settings import KEY_POSTS_LIST
from services.queryset import qs_definition
from users.serializers import AuthorDetailSerializer


class TagsSerializerMixin(serializers.ModelSerializer):
    """
    Миксин для сериализаторов, добавляющий поле tags для оптимизированного отображения тегов.
    Класс обеспечивает работу с предзагруженными данными тегов, сокращая количество запросов к базе данных
    """

    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        """
        Возвращает список тегов для поста в формате {"name": "наименование тега", "url": "URL тега"},
        используя предзагруженные данные, если они доступны
        """
        if hasattr(obj, 'prefetched_tags'):
            return [{'name': item.tag.name, 'url': item.tag.slug} for item in obj.prefetched_tags]
        return [{'name': tag.name, 'url': tag.slug} for tag in obj.tags.all()]


class PostsSerializer(TagsSerializerMixin, serializers.ModelSerializer):
    """Посты блога"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = AuthorDetailSerializer(fields=('id', 'username'))
    ncomments = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Post
        exclude = ('created', 'updated', 'draft', 'video', 'title_ru', 'title_en', 'body_en', 'body_ru')


class VideoDetailSerializer(serializers.ModelSerializer):
    """Видеозапись"""

    class Meta:
        model = Video
        fields = ('title', 'file')


class CommentsSerializer(serializers.ModelSerializer):
    """Вывод комментариев к постам"""

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        """
        Возвращает вложенные комментарии второго уровня для комментария первого уровня.

        Метод проверяет, есть ли предзагруженные данные для комментариев второго уровня
        в атрибуте `prefetched_comments2`. Если данные есть, они сериализуются и возвращаются.
        Если данных нет, возвращается пустой список, что означает отсутствие данных,
        а не ошибку в предзагрузке.
        """

        if hasattr(obj, 'prefetched_comments2'):
            return CommentsSerializer(obj.prefetched_comments2, many=True, context=self.context).data
        return []

    class Meta:
        model = Comment
        exclude = ('email', 'active', 'parent')


class AddCommentSerializer(serializers.ModelSerializer):
    """Добавление комментария к посту"""

    def validate(self, attrs):
        """Запрет на добавление комментария к черновым или ещё не опубликованным постам"""
        if attrs['post'].draft or attrs['post'].publish > timezone.now():
            raise serializers.ValidationError(_('Невозможно оставить комментарий для данного поста.'))
        return attrs

    def validate_parent(self, parent):
        """
        Проверяет, что:
        - Родительский комментарий не имеет собственного родителя (ограничение вложенности комментариев до 2 уровня)
        - Ответ можно добавить только к комментарию, который принадлежит тому же посту, что и сам ответ
        """
        if parent:

            if parent.parent:
                raise serializers.ValidationError(_('Нельзя добавлять комментарии третьего уровня вложенности.'))

            if not Comment.objects.filter(id=parent.id, post_id=self.initial_data['post']).exists():
                raise serializers.ValidationError('Нельзя добавлять ответ к комментарию другого поста.')

        return parent

    class Meta:
        model = Comment
        exclude = ('active',)


class PostDetailSerializer(TagsSerializerMixin, serializers.ModelSerializer):
    """Отдельный пост"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = AuthorDetailSerializer(fields=('id', 'username'))
    video = VideoDetailSerializer(read_only=True)
    ncomments = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Post
        exclude = ('draft', 'title_ru', 'title_en', 'body_ru', 'body_en')


class CategoryListSerializer(serializers.ModelSerializer):
    """Список категорий"""

    class Meta:
        model = Category
        exclude = ('name_ru', 'name_en', 'description_ru', 'description_en')


class VideoListSerializer(serializers.ModelSerializer):
    """Список видеозаписей"""

    post_video = PostDetailSerializer(read_only=True, fields=('id', 'url', 'category', 'author', 'tags'))
    ncomments = serializers.IntegerField()

    class Meta:
        model = Video
        exclude = ('title_ru', 'title_en', 'description_ru', 'description_en')


class RatingDetailSerializer(serializers.ModelSerializer):
    """Отдельный объект рейтинга"""

    class Meta:
        model = Rating
        fields = ('mark',)


class AddRatingSerializer(serializers.ModelSerializer):
    """Создание/обновление рейтинга к посту"""

    # queryset обеспечивает валидацию: запрещает добавлять оценку к черновикам и неопубликованным постам
    post = serializers.SlugRelatedField(slug_field='url', queryset=qs_definition(KEY_POSTS_LIST))

    class Meta:
        model = Rating
        fields = ('mark', 'post')

    def to_internal_value(self, data):
        """Автоматически добавляет slug в поле post из контекста"""
        data['post'] = self.context['slug']
        return super().to_internal_value(data)

    def create(self, validated_data):
        return Rating.objects.create(
            ip=validated_data['ip'],
            mark=validated_data['mark'],
            post=validated_data['post'],
        )

    def update(self, instance, validated_data):
        instance.mark = validated_data.get('mark', instance.mark)
        instance.save()
        return instance


class TopTagsSerializer(serializers.ModelSerializer):
    npost = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = '__all__'
