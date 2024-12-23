from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_by_me_DRF.settings import EMAIL_HOST_USER
from company.models import About
from company.serializers import AboutSerializer, ContactSerializer


def send(user_mail):
    """Отправка электронного письма при получении обратной связи через форму"""
    send_mail(
        'Запрос к администрации веб-приложения MAXFIELD.',
        'Ваш запрос зарегистрирован. Ожидайте обратную связь на данный адрес эл. почты. ',
        EMAIL_HOST_USER,
        [user_mail],
        fail_silently=False,
    )


class AboutView(APIView):
    """Вывод информации о компании"""

    def get(self, request):
        about = get_object_or_404(About)
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
                {'message': 'Сообщение успешно отправлено администрации проекта.'}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
