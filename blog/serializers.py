from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from blog.models import Post


class PostsSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Посты блога"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        exclude = ('created', 'updated', 'draft', 'video')
