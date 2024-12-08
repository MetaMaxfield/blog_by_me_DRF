from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from taggit.models import Tag

from blog.models import Category, Comment, Post, Rating, Video
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
        exclude = ('created', 'updated', 'draft', 'video')


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
        Проверяет, что родительский комментарий не имеет собственного родителя
        (исключение третьего уровня вложенности комментариев)
        """
        if parent and parent.parent:
            raise serializers.ValidationError(_('Нельзя добавлять комментарии третьего уровня вложенности.'))
        return parent

    class Meta:
        model = Comment
        fields = '__all__'


class PostDetailSerializer(TagsSerializerMixin, serializers.ModelSerializer):
    """Отдельный пост"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = AuthorDetailSerializer(fields=('id', 'username'))
    video = VideoDetailSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    ncomments = serializers.IntegerField()
    user_rating = serializers.IntegerField()

    def get_comments(self, obj):
        """
        Возвращает список комментариев для поста,
        используя предзагруженные данные в атрибуте 'prefetched_comments1'
        """
        return CommentsSerializer(obj.prefetched_comments1, context=self.context, read_only=True, many=True).data

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
        exclude = ('draft',)


class CategoryListSerializer(serializers.ModelSerializer):
    """Список категорий"""

    class Meta:
        model = Category
        fields = '__all__'


class VideoListSerializer(serializers.ModelSerializer):
    """Список видеозаписей"""

    post_video = PostDetailSerializer(read_only=True, fields=('id', 'url', 'category', 'author', 'tags'))
    ncomments = serializers.IntegerField()

    class Meta:
        model = Video
        fields = '__all__'


class AddRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к посту"""

    class Meta:
        model = Rating
        fields = ('mark', 'post')

    def validate(self, attrs):
        """Запрет на добавление оценки к черновым или ещё не опубликованным постам"""
        if attrs['post'].draft or attrs['post'].publish > timezone.now():
            raise serializers.ValidationError(_('Невозможно оставить оценку для данного поста.'))
        return attrs

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
