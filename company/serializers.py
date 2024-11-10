from rest_framework import serializers

from company.models import About, Contact


class AboutSerializer(serializers.ModelSerializer):
    """Информация о компании"""

    class Meta:
        model = About
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    """Обратная связь"""

    class Meta:
        model = Contact
        fields = '__all__'
