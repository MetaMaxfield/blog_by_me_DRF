from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from blog.models import Comment, Post, Video


class PostsSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Посты блога"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tags = TagListSerializerField()

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

    class Meta:
        model = Comment
        exclude = ('email', 'active')


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

    class Meta:
        model = Post
        exclude = ('draft',)
