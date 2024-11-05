from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import About
from company.serializers import AboutSerializer


class AboutView(APIView):
    """Вывод информации о компании"""

    def get(self, request):
        about = get_object_or_404(About)
        serializer = AboutSerializer(about)
        return Response(serializer.data)
