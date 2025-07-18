![gif-logo](https://github.com/MetaMaxfield/blog_by_me_DRF/raw/master/Blog-by-Me-DRF.gif)

<h1>
    <img align="left" src='https://github.com/MetaMaxfield/blog_by_me_DRF/raw/master/static/site_logo.png?raw=true' width="53.5" height="48.72" alt="logo">
    Блог "MAXFIELD" – Backend API
</h1>

![Static Badge](https://img.shields.io/badge/Python-3.11-blue?logo=python&labelColor=black)
![Static Badge](https://img.shields.io/badge/Django-4.2-lightgrey?logo=Django&labelColor=darkgreen)
![Static Badge](https://img.shields.io/badge/DRF-3.15-E5E5E5?logo=Django&labelColor=8B0000)
![Static Badge](https://img.shields.io/badge/PostgreSQL-%231f618d?logo=postgresql&logoColor=white)
![Static Badge](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white)
![Static Badge](https://img.shields.io/badge/Memcached-%2316a085)


Веб-проект с реализованным backend API на Django REST Framework.

## Содержание:

- [Инструменты](#используемые-технологии-и-инструменты)
- [Функционал](#реализованный-функционал)
- [Особенности](#особенности-проекта)
- [Структура](#структура-проекта-директории-и-файлы)
- [Установка](#установка)
- [Источники](#источники)

## Используемые технологии и инструменты:

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Django 4.2.1](https://docs.djangoproject.com/en/4.2/)
- [Django REST Framework 3.15.2](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Memcached](https://memcached.org/)
- [SMTP Gmail](https://myaccount.google.com/apppasswords)
- [Docker](https://www.docker.com/)

## Реализованный функционал:

- Система пользователей (Гость, Автор, Модератор, Администратор);
- Панель администратора с разграничением прав доступа по ролям пользователей;
- Система постов с архитектурой блога;
- Категории и теги к постам;
- Фильтрация постов по категориям, тегам и дате публикации;
- Поиск постов по названию или содержанию;
- Поэтапное отображение данных (пагинация);
- Комментарии к постам и ответы к ним;
- Система рейтинга постов;
- Возможность задать вопрос авторам блога с ответом на e-mail;
- Отложенная публикация постов;
- Мультиязычность (Русский, Английский).

## Особенности проекта:

- Версионирование API;
- Документирование API;
- Представления на базе ViewSet-ов, generic‑классов и APIView;
- Отдельные сериализаторы для каждого действия;
- Полнотекстовый поиск на основе векторного сопоставления с ранжированием результатов по релевантности;
- Маршрутизация URL через стандартные пути и роутеры DRF;
- Поддерживаемость различных типов пагинации с возможностью выбора типа для списка постов через параметр запроса;
- Частично интегрированный специализированный рендеринг API;
- Поддерживаемость CORS;
- Промежуточное ПО (middleware) для автоматической установки русского языка в панели администратора;
- Пользовательское исключение для быстрой обработки отсутствия результатов поиска;
- Использование IP пользователей в системе рейтинга постов;
- Пользовательские валидаторы параметров и полей модели;
- Автоудаление неиспользуемых медиафайлов (с помощью сигналов);
- Оптимизация запросов к базе данных;
- Кэширование отдельных данных;
- Получение данных из кэша или БД по ключам из переменных виртуального окружения;
- Расширение функциональности шаблонов панели администрирования;
- Вынесение бизнес-логики в сервисный слой для повышения читаемости и поддержки кода;
- Debug‑toolbar для отладки в процессе разработки;
- Логгирование уровней WARNING и ERROR в отдельный файл для отслеживания ошибок в пользовательской логике;
- Пользовательские команды для упрощения рутинных операций и администрирования проекта:
    * Создание расширенной плоской страницы с информацией о веб-проекте;
    * Создание необходимых групп пользователей;
    * Создание оценочных значений для системы рейтинга;
- Линтеры и форматтеры: black, isort, flake8 с настроенными pre-commit хуками;
- Интеграция библиотеки python-dotenv для работы с переменными окружения и хранения приватных параметров проекта;
- Готовые медиафайлы и данные БД для локальной разработки и ручного тестирования;
- Мультиплатформенность за счёт использования Docker для развёртывания базы данных и кэш‑сервиса;
- Автоматизированный скрипт для быстрого старта проекта:
    * Создание виртуального окружения;
    * Установка зависимостей;
    * Скачивание, распаковка и последующее удаление медиаархива для ручного тестирования;
    * Создание .env с необходимыми переменными;
    * Настройка pre-commit хуков;
    * Запуск контейнеров с БД и кэшем;
    * Запуск локального сервера;
- Юнит-тесты и интеграционные тесты на pytest с использованием фикстур, фабрик для генерации тестовых данных, отслеживанием покрытия кода и отдельной конфигурацией проекта для тестирования.

## Структура проекта (директории и файлы):
```
├── blog                                    # Пакет с приложением
│   ├── migrations                          # Пакет с миграциями
│   ├── admin.py                            # Файл с зарегистрированными моделями приложения в системе администрирования
│   ├── apps.py                             # Файл с конфигурацией приложения
│   ├── models.py                           # Файл с моделями данных приложения
│   ├── serializers.py                      # Файл с сериализаторами приложения
│   ├── signals.py                          # Файл с обработчиками сигналов приложения
│   ├── translation.py                      # Файл с обозначением полей моделей для локализации
│   ├── urls.py                             # Файл с шаблонами адресов проекта
│   └── views.py                            # Файл с логикой приложения
├── blog_by_me_DRF                          # Пакет с файлами проекта
│   ├── asgi.py                             # Файл с конфигурацией для расширения возможностей WSGI
│   ├── middleware.py                       # Файл для плагинов глобального изменения входных и выходных данных
│   ├── settings_test.py                    # Файл с конфигурацией проекта при тестировании
│   ├── settings.py                         # Файл с основной конфигурацией проекта
│   ├── urls.py                             # Файл с шаблонами адресов приложения 
│   └── wsgi.py                             # Файл с конфигурацией для запуска проекта как WSGI-приложения
├── common                                  # Пакет с приложением, файлы которого используются в нескольких других приложениях
│   └── management                          # Родительский пакет для пакета с файлами пользовательских команд
│       └── commands                        # Пакет с файлами пользовательских команд
│           ├── create_about_model.py       # Файл пользовательской команды создания записи "О компании"
│           ├── create_groups.py            # Файл пользовательской команды создания групп пользователей
│           └── create_mark_models.py       # Файл пользовательской команды создания оценок к постам
├── company                                 # Пакет с приложением
│   ├── migrations                          # Пакет с миграциями
│   ├── admin.py                            # Файл с зарегистрированными моделями приложения в системе администрирования
│   ├── apps.py                             # Файл с конфигурацией приложения
│   ├── models.py                           # Файл с моделями данных приложения
│   ├── serializers.py                      # Файл с сериализаторами приложения
│   ├── translation.py                      # Файл с обозначением полей моделей для локализации
│   ├── urls.py                             # Файл с шаблонами адресов приложения
│   └── views.py                            # Файл с логикой приложения
├── db_init                                 # Директория инициализации тестовой базы данных
│   └── backup.sql                          # Файл для инициализации тестовой базы данных
├── locale                                  # Директория с локализацией
├── logs                                    # Директория с файлами для логгирования
│   └── user_commands.log                   # Файл с логами ошибок и предупреждений пользовательских команд
├── media                                   # Директория с изображениями и видеофайлами, которые добавляются при создании модели
├── services                                # Пакет с сервисным слоем приложений
│   ├── blog                                # Пакет с сервисным слоем приложения "blog"
│   │   ├── paginators.py                   # Файл с модулем пагинации
│   │   └── validators.py                   # Файл с модулем валидаторов проверки входных параметров
│   ├── company                             # Пакет с сервисным слоем приложения "company"
│   │   └── send_mail.py                    # Файл с модулем отправки сообщений через e-mail
│   ├── users                               # Пакет с сервисным слоем приложения "users"
│   │   └── validator.py                    # Файл с модулем валидатора поля модели приложения
│   ├── caching.py                          # Файл с модулем кэширования
│   ├── client_ip.py                        # Файл с модулем получения ip пользователя
│   ├── exceptions.py                       # Файл с модулем пользовательских исключений
│   ├── queryset.py                         # Файл с модулем чтения данных из базы данных
│   ├── rating.py                           # Файл с модулем добавления рейтинга
│   ├── renderer.py                         # Файл с модулем специализированного рендеринга API
│   └── search.py                           # Файл с модулем поиска
├── static                                  # Директория для хранения статических файлов
├── templates                               # Директория с HTML-шаблонами административной панели
├── tests                                   # Пакет с тестами проекта
│   ├── blog                                # Пакет с тестами приложения "blog"
│   │   ├── conftest.py                     # Файл с фикстурами для данного пакета
│   │   ├── factories.py                    # Файл с фабриками моделей
│   │   ├── test_models.py                  # Файл с тестами моделей
│   │   └── test_serializers.py             # Файл с тестами сериализаторов
│   ├── company                             # Пакет с тестами приложения "company"
│   │   ├── factories.py                    # Файл с фабриками моделей
│   │   └── test_serializers.py             # Файл с тестами сериализаторов
│   ├── services                            # Пакет с тестами сервисного слоя
│   └── users                               # Пакет с тестами приложения "users"
│       ├── conftest.py                     # Файл с фикстурами для данного пакета
│       ├── factories.py                    # Файл с фабриками моделей
│       └── test_views.py                   # Файл с тестами представлений
├── users                                   # Пакет с приложением
│   ├── migrations                          # Пакет с миграциями
│   ├── admin.py                            # Файл с зарегистрированными моделями приложения в системе администрирования
│   ├── apps.py                             # Файл с конфигурацией приложения
│   ├── models.py                           # Файл с моделями данных приложения
│   ├── serializers.py                      # Файл с сериализаторами приложения
│   ├── signals.py                          # Файл с обработчиками сигналов приложения
│   ├── translation.py                      # Файл с обозначением полей моделей для локализации
│   ├── urls.py                             # Файл с шаблонами адресов приложения 
│   └── views.py                            # Файл с логикой приложения
├── .env                                    # Файл с переменными окружения (добавляется через запуск setup_dev.py)
├── .gitattributes                          # Файл с атрибутами Git
├── .gitignore                              # Файл для списка файлов и папок, которые Git игнорирует и не отслеживает
├── .pre-commit-config.yaml                 # Файл конфигурации для настройки хуков pre-commit
├── Blog-by-Me-DRF.gif                      # GIF-изображение с логотипом проекта
├── docker-compose.yaml                     # Файл конфигурации для запуска контейнеров
├── manage.py                               # Файл-утилита командной строки для управления проектом
├── pyproject.toml                          # Файл конфигурации для форматера кода black
├── pytest.ini                              # Файл конфигурации для тестирования с pytest
├── README.md                               # Файл с руководством описания проекта
├── requirements.txt                        # Файл с названиями модулей и пакетов для корректной работы проекта
├── setup_dev.py                            # Скрипт-файл для старта локальной разработки
└── setup.cfg                               # Файл конфигурации для линтера кода flake8 и организатора импортов isort
```

## Установка:

1. Копируем содержимое репозитория (требуется установленный [Git](https://git-scm.com/downloads))

    ```
    git clone https://github.com/MetaMaxfield/blog_by_me_DRF.git
    ```
   
2. Добавляем проект в приложения Google аккаунта и сохраняем пароль приложения

3. Запускаем Docker Desktop

4. Выполним автоматическую подготовку проекта к локальной разработке

    - Запускаем через консоль файл setup_dev.py
      ```
      python setup_dev.py
      ```
   
   - В процессе настройки переменных окружения нужно добавить следующие значения:
   
     Пример: ``` SECRET_KEY=your_secret_key ```

     ```
     # Список переменных окружения, значения которых мы сохраняли ранее:
     EMAIL_HOST_USER_KEY=         # Почта Google аккаунта для отправки e-mail 
     EMAIL_HOST_PASSWORD_KEY=     # Пароль от приложения из Google аккаунта
     KEY_DATABASES_USER=          # Имя пользователя в PostgreSQL
     KEY_DATABASES_PASSWORD=      # Пароль пользователя в PostgreSQL
     ```
     
5. Проект готов к локальной разработке. Локальный сервер запущен автоматически.

## Источники:
1. [Документация Python 3.11](https://docs.python.org/3.11/)
2. [Документация Django 4.2](https://docs.djangoproject.com/en/4.2/)
3. [Документация Django REST Framework](https://www.django-rest-framework.org/)
4. [Документация Docker](https://docs.docker.com/reference/)
5. [Руководство по тестированию](https://developer.mozilla.org/ru/docs/Learn_web_development/Extensions/Server-side/Django/Testing)
6. Книга "Django 2 в примерах" А. Меле
7. [YouTube канал "Михаил Омельченко"](https://www.youtube.com/@DjangoSchool)
8. [ChatGPT-4o от OpenAI](https://chatgpt.com/)
