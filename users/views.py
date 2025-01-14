from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_by_me_DRF.settings import KEY_AUTHOR_DETAIL, KEY_AUTHORS_LIST
from services.caching import get_cached_objects_or_queryset
from users.serializers import AuthorDetailSerializer, AuthorListSerializer

# class AuthorListView(APIView):
#     """Вывод списка авторов"""
#
#     def get(self, request: Request) -> Response:
#         author_list = get_cached_objects_or_queryset(KEY_AUTHORS_LIST)
#         authors_serializer = AuthorListSerializer(author_list, many=True)
#         return Response(authors_serializer.data)


class AuthorListView(generics.ListAPIView):
    """Вывод списка авторов"""

    serializer_class = AuthorListSerializer

    def get_queryset(self):
        return get_cached_objects_or_queryset(KEY_AUTHORS_LIST)


class AuthorDetailView(APIView):
    """Вывод данных об авторе"""

    def get(self, request: Request, pk: int) -> Response:
        author = get_cached_objects_or_queryset(KEY_AUTHOR_DETAIL, pk=pk)
        author_serializer = AuthorDetailSerializer(author)
        return Response(author_serializer.data)
