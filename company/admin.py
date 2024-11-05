from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from company.models import About


class DescriptionAdminForm(forms.ModelForm):
    """Ckeditor для поля "description" модели About"""

    description = forms.CharField(label='Основной текстовый контент страницы', widget=CKEditorUploadingWidget())

    class Meta:
        model = About
        fields = '__all__'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """Страница «О нас»"""

    form = DescriptionAdminForm
    fieldsets = (
        ('Информация', {'fields': ('description',)}),
        ('Электронная почта для связи', {'fields': ('email_contact',)}),
        ('Телефоны для связи', {'description': 'Пример: +79099099900', 'fields': ('phone1_num', 'phone2_num')}),
        (
            'Местонахождение компании',
            {
                'description': 'Добавьте полный адрес вашей компании и '
                'географические координаты (широта и долгота) '
                'для отображения на карте.',
                'fields': ('address', ('latitude', 'longitude')),
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        """
        Перенаправление на страницу редактирования объекта модели About
        при существовании единственного экземпляра модели
        """
        try:
            about = About.objects.get()
            return self.change_view(request, object_id=str(about.pk))
        except ObjectDoesNotExist:
            return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        """Запрет на добавление объектов модели вне зависимости от статуса пользователя"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Запрет на удаление объектов модели вне зависимости от статуса пользователя"""
        return False
