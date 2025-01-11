from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Регистрирует обработчики сигналов при инициализации приложения"""
        import users.signals
