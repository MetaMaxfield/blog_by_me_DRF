from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from blog.models import Category, Comment, Post, Rating, Video


class PostsSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Посты блога"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tags = TagListSerializerField()
    ncomments = serializers.IntegerField()

    class Meta:
        model = Post
        exclude = ('created', 'updated', 'draft', 'video')


class VideoDetailSerializer(serializers.ModelSerializer):
    """Видеозапись"""

    class Meta:
        model = Video
        fields = ('title', 'file')


class FilterCommentsListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentsSerializer(serializers.ModelSerializer):
    """Вывод комментариев к постам"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentsListSerializer
        model = Comment
        exclude = ('email', 'active', 'parent')


class AddCommentSerializer(serializers.ModelSerializer):
    """Добавление комментария к посту"""

    class Meta:
        model = Comment
        fields = '__all__'


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Отдельный пост"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    video = VideoDetailSerializer(read_only=True)
    tags = TagListSerializerField()
    comments = CommentsSerializer(read_only=True, many=True)
    ncomments = serializers.IntegerField()
    user_rating = serializers.IntegerField()

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

    post_video = PostDetailSerializer(read_only=True, fields=('id', 'url', 'category'))
    ncomments = serializers.IntegerField()

    class Meta:
        model = Video
        fields = '__all__'


class AddRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к посту"""

    class Meta:
        model = Rating
        fields = ('mark', 'post')

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
