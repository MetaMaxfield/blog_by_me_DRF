from django.core.cache import cache
from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import TaggedItem

from blog.models import Post
from blog_by_me_DRF.settings import CACHE_KEY, CACHE_TIMES, KEY_AUTHOR_DETAIL, KEY_AUTHORS_LIST
from users.models import User
from users.serializers import AuthorDetailSerializer, AuthorListSerializer


class AuthorListView(APIView):
    """Вывод списка авторов"""

    def get(self, request):

        author_list = cache.get(f'{CACHE_KEY}{KEY_AUTHORS_LIST}')

        if not author_list:
            author_list = User.objects.all().only('id', 'username', 'image', 'description')
            cache.set(f'{CACHE_KEY}{KEY_AUTHORS_LIST}', author_list, CACHE_TIMES[KEY_AUTHORS_LIST])

        authors_serializer = AuthorListSerializer(author_list, many=True)
        return Response(authors_serializer.data)


class AuthorDetailView(APIView):
    """Вывод данных об авторе"""

    def get(self, request, pk):

        author = cache.get(f'{CACHE_KEY}{KEY_AUTHOR_DETAIL}{pk}')

        if not author:

            author = get_object_or_404(
                User.objects.annotate(
                    nposts=Count(
                        'post_author', filter=Q(post_author__draft=False, post_author__publish__lte=timezone.now())
                    )
                )
                .prefetch_related(
                    Prefetch(
                        'post_author',
                        Post.objects.filter(draft=False, publish__lte=timezone.now())
                        .order_by('-publish', '-id')
                        .select_related('category')
                        .prefetch_related(
                            Prefetch(
                                'tagged_items', TaggedItem.objects.select_related('tag'), to_attr='prefetched_tags'
                            )
                        )[:3],
                        to_attr='last_3_posts',
                    )
                )
                .defer('password', 'last_login', 'is_active', 'is_staff'),
                id=pk,
            )

            cache.set(f'{CACHE_KEY}{KEY_AUTHOR_DETAIL}{pk}', author, CACHE_TIMES[KEY_AUTHOR_DETAIL])

        author_serializer = AuthorDetailSerializer(author)
        return Response(author_serializer.data)
