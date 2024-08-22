from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostsSerializer


class PostsView(APIView):
    """Вывод постов блога"""

    def get(self, request):
        object_list = (
            Post.objects.filter(draft=False)
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
        )
        serializer = PostsSerializer(object_list, many=True)
        return Response(serializer.data)
