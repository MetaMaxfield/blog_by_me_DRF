from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_by_me_DRF.settings import CACHE_KEY, CACHE_TIMES, KEY_AUTHOR_DETAIL, KEY_AUTHORS_LIST
from services.queryset import qs_definition
from users.serializers import AuthorDetailSerializer, AuthorListSerializer


class AuthorListView(APIView):
    """Вывод списка авторов"""

    def get(self, request):
        author_list = cache.get(f'{CACHE_KEY}{KEY_AUTHORS_LIST}')

        if not author_list:
            author_list = qs_definition(KEY_AUTHORS_LIST)
            cache.set(f'{CACHE_KEY}{KEY_AUTHORS_LIST}', author_list, CACHE_TIMES[KEY_AUTHORS_LIST])

        authors_serializer = AuthorListSerializer(author_list, many=True)
        return Response(authors_serializer.data)


class AuthorDetailView(APIView):
    """Вывод данных об авторе"""

    def get(self, request, pk):
        author = cache.get(f'{CACHE_KEY}{KEY_AUTHOR_DETAIL}{pk}')

        if not author:
            author = qs_definition(KEY_AUTHOR_DETAIL, pk=pk)
            cache.set(f'{CACHE_KEY}{KEY_AUTHOR_DETAIL}{pk}', author, CACHE_TIMES[KEY_AUTHOR_DETAIL])

        author_serializer = AuthorDetailSerializer(author)
        return Response(author_serializer.data)
