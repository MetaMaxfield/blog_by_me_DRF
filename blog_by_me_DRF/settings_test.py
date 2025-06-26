import os

from blog_by_me_DRF.settings import *

# Настройки кэша при тестировании
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Способ для отправки электронных писем при тестировании в django.core.mail
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Логирование для тестирования
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# Путь файловой системы к каталогу с файлами при тестировании
MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'test_media')
