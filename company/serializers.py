from rest_framework import serializers

from company.models import About


class AboutSerializer(serializers.ModelSerializer):
    """Информация о компании"""

    class Meta:
        model = About
        fields = '__all__'
