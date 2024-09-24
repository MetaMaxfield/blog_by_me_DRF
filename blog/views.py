from django.db.models import Count, Prefetch
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Category, Post, Video
from blog.serializers import (
    AddCommentSerializer,
    CategoryListSerializer,
    PostDetailSerializer,
    PostsSerializer,
    VideoListSerializer,
)


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


class AddCommentView(APIView):
    """Добавление комментария к посту"""

    def post(self, request):
        comment = AddCommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)


class PostDetailView(APIView):
    """Вывод отдельного поста"""

    def get(self, request, slug):
        post = get_object_or_404(
            Post.objects.filter(draft=False).defer('draft').annotate(ncomments=Count('comments')), url=slug
        )
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class CategoryListView(APIView):
    """Вывод списка категорий и постов к ним"""

    def get(self, request):
        category_list = Category.objects.all()
        category_serializer = CategoryListSerializer(category_list, many=True)
        post_list = (
            Post.objects.filter(draft=False)
            .select_related('category')
            .prefetch_related(
                'tagged_items__tag',
            )
            .defer('video', 'created', 'updated', 'draft')
            .annotate(ncomments=Count('comments'))
        )
        posts_serializer = PostsSerializer(post_list, many=True)
        return Response(
            {
                'category_list': category_serializer.data,
                'post_list': posts_serializer.data,
            }
        )


class VideoListView(APIView):
    """Вывод всех видеозаписей"""

    def get(self, request):
        video_list = (
            Video.objects.filter(post_video__draft=False)
            .select_related('post_video')
            .prefetch_related(
                Prefetch('post_video__category', Category.objects.only('id', 'name')),
            )
            .annotate(
                ncomments=Count('post_video__comments'),
            )
            .order_by('-create_at')
        )
        videos_serializer = VideoListSerializer(video_list, many=True)
        return Response(videos_serializer.data)
