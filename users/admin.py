from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from users.models import User


@admin.register(User)
class UserAdmin(TranslationAdmin, UserAdmin):
    """Расширенная модель пользователя"""

    model = User
    list_display = ('username', 'email', 'get_user_groups', 'is_superuser', 'get_image')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    readonly_fields = ['get_image', 'last_login', 'date_joined']
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [
            ('Персональная информация'),
            {'fields': ('first_name', 'last_name', 'email', 'birthday', 'description', ('image', 'get_image'))},
        ],
        [
            ('Список разрешений'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ],
        [('Важные даты'), {'fields': ('last_login', 'date_joined')}],
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    def get_image(self, obj):
        """Отображение изображения в панеле администрации"""
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100", height="100"')
        return 'Нет изображения'

    get_image.short_description = 'Изображение'

    def get_fieldsets(self, request, obj=None):
        """Отображение полей в зависимости от статуса пользователя"""
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets
        elif request.user.id == obj.id:
            fields = fieldsets.copy()
            fields[0][1]['fields'] = ['username', 'password']
            fields.pop(2)
            return fields
        else:
            fields = fieldsets.copy()
            fields[0][1]['fields'] = [
                'username',
            ]
            fields.pop(2)
            return fields

    def has_change_permission(self, request, obj=None):
        """
        Разрешение на редактирование модели только суперпользователю
        или владельцу
        """
        if request.user.is_superuser or request.user == obj:
            return True
        else:
            return False
