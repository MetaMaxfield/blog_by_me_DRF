from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import AuthorDetailSerializer, AuthorListSerializer


class AuthorListView(APIView):
    """Вывод списка авторов"""

    def get(self, request):
        author_list = User.objects.all().only('id', 'username', 'image', 'description')
        authors_serializer = AuthorListSerializer(author_list, many=True)
        return Response(authors_serializer.data)


class AuthorDetailView(APIView):
    """Вывод данных об авторе"""

    def get(self, request, pk):
        author = get_object_or_404(
            User.objects.annotate(
                nposts=Count(
                    'post_author', filter=Q(post_author__draft=False, post_author__publish__lte=timezone.now())
                )
            ).defer('password', 'last_login', 'is_active', 'is_staff'),
            id=pk,
        )
        author_serializer = AuthorDetailSerializer(author)
        return Response(author_serializer.data)
