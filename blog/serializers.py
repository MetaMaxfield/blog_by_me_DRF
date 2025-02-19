from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from taggit.models import Tag

from blog.models import Category, Comment, Mark, Post, Rating, Video
from services.client_ip import get_client_ip
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
        if parent and parent.parent:
            raise serializers.ValidationError(_('Нельзя добавлять комментарии третьего уровня вложенности.'))

        if not Comment.objects.filter(id=parent.id, post_id=self.initial_data['post']).exists():
            raise serializers.ValidationError(_('Нельзя добавлять ответ к комментарию другого поста.'))

        return parent

    class Meta:
        model = Comment
        exclude = ('active',)


class PostDetailSerializer(TagsSerializerMixin, serializers.ModelSerializer):
    """Отдельный пост"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = AuthorDetailSerializer(fields=('id', 'username'))
    video = VideoDetailSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    ncomments = serializers.IntegerField()
    user_rating = serializers.SerializerMethodField()

    def get_comments(self, obj):
        """
        Возвращает список комментариев для поста,
        используя предзагруженные данные в атрибуте 'prefetched_comments1'
        """
        return CommentsSerializer(obj.prefetched_comments1, context=self.context, read_only=True, many=True).data

    def get_user_rating(self, obj):
        """
        Определяет устанавливал ли пользователь рейтинг к посту
        и возвращает id оценки или None
        """
        received_ip = get_client_ip(self.context['request'])
        try:
            user_rating = Mark.objects.get(rating_mark__ip=received_ip, rating_mark__post=obj).id
        except Mark.DoesNotExist:
            user_rating = None
        return user_rating

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
