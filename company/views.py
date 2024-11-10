from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import About, Contact
from company.serializers import AboutSerializer, ContactSerializer


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
            return Response(
                {'message': 'Сообщение успешно отправлено администрации проекта.'}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
