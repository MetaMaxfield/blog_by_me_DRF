from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        """Регистрирует обработчики сигналов при инициализации приложения"""
        import blog.signals
