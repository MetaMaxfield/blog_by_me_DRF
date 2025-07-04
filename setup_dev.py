import os
import platform
import subprocess
import sys
import tarfile
import time
import venv
from urllib.request import urlretrieve

RESTARTED_FILE = os.getenv('RESTARTED_FILE') == 'True'
ARCHIVE_URL = "https://github.com/MetaMaxfield/blog_by_me_DRF/releases/download/test-media/media.tar.gz"
ARCHIVE_NAME = "media.tar.gz"
UNPACK_DIR = "./media"
VARIABLES_WITH_RANDOM_VALUES = (
    'CACHE_KEY',
    'KEY_SIMPLE_POSTS_LIST',
    'KEY_POSTS_LIST',
    'KEY_POST_DETAIL',
    'KEY_CATEGORIES_LIST',
    'KEY_VIDEOS_LIST',
    'KEY_ABOUT',
    'KEY_AUTHORS_LIST',
    'KEY_AUTHOR_DETAIL',
    'KEY_AUTHOR_DETAIL_STRICT',
    'KEY_TOP_POSTS',
    'KEY_LAST_POSTS',
    'KEY_ALL_TAGS',
    'KEY_RATING_DETAIL',
    'KEY_MARK_DETAIL',
    'KEY_POSTS_CALENDAR',
    'KEY_COMMENTS_LIST',
)
DATABASE_NAME = 'blog_by_me_DRF'
VARIABLES_WITH_SET_VALUES = (
    'EMAIL_HOST_USER_KEY',
    'EMAIL_HOST_PASSWORD_KEY',
    'KEY_DATABASES_USER',
    'KEY_DATABASES_PASSWORD',
)
VENV_PYTHON = 'venv\\Scripts\\python.exe' if platform.system() == 'Windows' else 'venv/bin/python'


registry = []


def register(stage):
    """Помечает функцию как этап 'pre' или 'post' для последовательного запуска"""

    def add_func(func):
        registry.append((func, stage))
        return func

    return add_func


def main():
    """Запускает функции из registry в зависимости от стадии (pre/post перезапуска)"""
    for func, stage in registry:
        if (not RESTARTED_FILE and stage == 'pre') or (RESTARTED_FILE and stage == 'post'):
            func()


@register('pre')
def _create_venv():
    print('Создание виртуального окружения...')
    venv.create('venv', with_pip=True)
    print('Виртуальное окружение создано.')
    print()


@register('pre')
def _pip_install_requirements():
    print('Установка зависимостей...')
    subprocess.run([VENV_PYTHON, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    print('Зависимости установлены.')
    print()


@register('pre')
def _restart_file():
    print('Перезапуск файла для применения зависимостей...')
    new_env = os.environ.copy()
    new_env['RESTARTED_FILE'] = 'True'

    # Запускаем дочерний процесс в venv и ждём его
    subprocess.run([VENV_PYTHON, __file__], env=new_env, check=True)
    # Затем завершаем родительский процесс
    sys.exit(0)


@register('post')
def _install_media_archive():
    print('Файл перезапущен.')
    print()

    print('Скачивание архива с медиафайлами...')
    urlretrieve(ARCHIVE_URL, ARCHIVE_NAME)
    print('Скачивание архива с медиафайлами завершено.')
    print()


@register('post')
def _unpack_media_archive():
    print(f'Распаковка архива в {UNPACK_DIR}...')
    with tarfile.open(ARCHIVE_NAME, 'r:gz') as tar:
        tar.extractall(UNPACK_DIR)
    print('Распаковка архива завершена.')
    print()


@register('post')
def _delete_archive():
    print('Удаление архива...')
    os.remove(ARCHIVE_NAME)
    print('Удаление архива завершено.')
    print()


@register('post')
def _generate_env_variables():
    from django.utils.crypto import get_random_string
    from dotenv import set_key

    print('Создание файла .env и генерация переменных окружения...')
    for key in VARIABLES_WITH_RANDOM_VALUES:
        set_key('.env', key, get_random_string(5))
    print('Файл .env и переменные окружения созданы.')
    print()


@register('post')
def _auto_set_env_database_name():
    from dotenv import set_key

    print('Автодобавление переменной с наименованием БД...')
    set_key('.env', 'KEY_DATABASES_NAME', DATABASE_NAME)
    print('Переменная окружения добавлена.')
    print()


@register('post')
def _set_env_variables():
    from dotenv import set_key

    print('Добавление переменных окружения...')
    for key in VARIABLES_WITH_SET_VALUES:
        set_key('.env', key, input(f'\tВведите значение для переменной {key}: '))
    print('Переменные окружения добавлены.')
    print()


@register('post')
def _generate_secret_key():
    from django.core.management.utils import get_random_secret_key
    from dotenv import set_key

    print('Генерация DJANGO_SECRET_KEY...')
    set_key('.env', 'DJANGO_SECRET_KEY', get_random_secret_key())
    print('Переменная DJANGO_SECRET_KEY создана.')
    print()


@register('post')
def _pre_commit_install():
    print('Определение pre-commit хуков...')
    subprocess.run([VENV_PYTHON, '-m', 'pre_commit', 'install'], check=True)
    print('Pre-commit хуки определены.')
    print()


@register('post')
def _start_docker_compose():
    print('Запуск базы данных и сервиса кэширования в контейнерах...')
    subprocess.run(['docker', 'compose', 'up', '-d', '--build'], check=True)
    print('База данных и сервис кэширования запущен.')
    print()


@register('post')
def _run_server():
    print('Запуск локального сервера...')
    time.sleep(5)
    subprocess.run([VENV_PYTHON, 'manage.py', 'runserver'], check=True)


if __name__ == '__main__':
    main()
