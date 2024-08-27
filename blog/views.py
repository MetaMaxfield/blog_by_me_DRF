from django.db.models import Count
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostDetailSerializer, PostsSerializer


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


class PostDetailView(APIView):
    """Вывод отдельного поста"""

    def get(self, request, slug):
        post = get_object_or_404(
            Post.objects.filter(draft=False).defer('draft').annotate(ncomments=Count('comments')), url=slug
        )
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
