from django.core.cache import cache
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_by_me_DRF.settings import CACHE_KEY, CACHE_TIMES, KEY_ABOUT
from company.serializers import AboutSerializer, ContactSerializer
from services.company.send_mail import send
from services.queryset import qs_about


class AboutView(APIView):
    """Вывод информации о компании"""

    def get(self, request):
        about = cache.get(f'{CACHE_KEY}{KEY_ABOUT}')
        if not about:
            about = qs_about()
            cache.set(f'{CACHE_KEY}{KEY_ABOUT}', about, CACHE_TIMES[KEY_ABOUT])
        serializer = AboutSerializer(about)
        return Response(serializer.data)


class ContactView(APIView):
    """Добавление сообщения обратной связи"""

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send(serializer.validated_data['email'])
            return Response(
                {'message': _('Сообщение успешно отправлено администрации проекта.')}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
