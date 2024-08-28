from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from blog.models import Post, Video


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


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Отдельный пост"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    video = VideoDetailSerializer(read_only=True)
    tags = TagListSerializerField()
    ncomments = serializers.IntegerField()

    class Meta:
        model = Post
        exclude = ('draft',)
