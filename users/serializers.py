from django.utils import timezone
from rest_framework import serializers

from users.models import User


class AuthorListSerializer(serializers.ModelSerializer):
    """Список авторов"""

    class Meta:
        model = User
        fields = ('id', 'username', 'image', 'description')


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Данные автора"""

    get_user_groups = serializers.ListField()
    nposts = serializers.IntegerField()
    last_posts = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_last_posts(self, obj):
        from blog.serializers import PostsSerializer

        return PostsSerializer(
            obj.post_author.filter(draft=False, publish__lte=timezone.now())
            .order_by('-publish', '-id')
            .select_related('category')[:3],
            many=True,
            fields=('title', 'category', 'url', 'body', 'image', 'publish'),
        ).data

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_permissions')
