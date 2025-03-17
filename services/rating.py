from django.utils.translation import gettext as _
from rest_framework import status

from blog.models import Mark, Rating
from blog_by_me_DRF.settings import KEY_AUTHOR_DETAIL_STRICT, KEY_MARK_DETAIL, KEY_RATING_DETAIL
from services.queryset import qs_definition
from users.models import User


class ServiceUserRating:
    """
    Класс для управления рейтингом автора user_rating на основе оценки (Mark) для поста.

    Взаимодействие с объектом класса осуществляется через
    existing_rating или update_author_rating_with_return_message_and_status_code()
    """

    RATING_UPDATE_MESSAGE = _('Рейтинг успешно обновлен.')
    RATING_CREATE_MESSAGE = _('Рейтинг успешно добавлен.')

    def __init__(self, ip: str, post_slug: str, mark_id: int, http_method: str) -> None:
        """
        Инициализация

        Атрибуты объекта:
        self.ip: Сохраняет IP-адрес оценивающего пользователя.
        self.post_slug: Сохраняет идентификатор поста.
        self.mark_id: Сохраняет идентификатор оценки.
        self.http_method: Определяет логику отсутствия рейтинга в сервисном слое:
            - Http404 для GET (retrieve)
            - None для POST (create/update)
        self._existing_rating: Внутренний атрибут, который может иметь три значения:
            - False: Запрос к базе данных на получение рейтинга ещё не выполнялся.
            - Rating: Экземпляр модели Rating, если рейтинг найден в базе данных.
            - None: Если рейтинг в базе данных не найден.
        """
        self.ip = ip
        self.post_slug = post_slug
        self.mark_id = mark_id
        self.http_method = http_method

        self._existing_rating = False

    @property
    def existing_rating(self) -> Rating | None:
        """
        Применяется как атрибут (используйте .existing_rating).

        Возвращает текущий рейтинг пользователя к посту.

        Особенности использования:
            1. Может быть вызван отдельно в представлении для проверки наличия существующего
               рейтинга или подтверждения его отсутствия (определение первичного оценивания),
               с последующей передачей в сериализатор.
            2. Вызывается автоматически внутри метода _update_rating()

        Логика работы:
            - Если запрос ещё не выполнялся (_existing_rating == False),
              метод выполняет запрос в базу данных.
            - Если запрос уже выполнялся, возвращается ранее полученное значение _existing_rating.
        """
        if self._existing_rating is False:
            self._existing_rating = qs_definition(
                KEY_RATING_DETAIL, ip=self.ip, post_slug=self.post_slug, http_method=self.http_method
            )
        return self._existing_rating

    def _get_mark(self) -> Mark:
        """Возвращает объект оценки (Mark) по указанному ID"""
        return qs_definition(KEY_MARK_DETAIL, pk=self.mark_id)

    def _get_author(self) -> User:
        """Возвращает объект автора (User) по указанному post_slug"""
        return qs_definition(KEY_AUTHOR_DETAIL_STRICT, post_slug=self.post_slug)

    def _get_message_and_status_code(self) -> tuple[str, int]:
        """
        Возвращает сообщение и статусный код в зависимости от действия с рейтингом.

        Логика:
            - Если _existing_rating содержит объект Rating, возвращается сообщение и код,
            означающие обновление оценки к посту.
            - Если _existing_rating равно None, возвращается сообщение и код, означающие добавление оценки к посту.

        _existing_rating обновляется в методе existing_rating после выполнения запроса к базе данных, и может
        служить индикатором для определения необходимого сообщения и HTTP-статуса.
        """
        if self._existing_rating:
            return ServiceUserRating.RATING_UPDATE_MESSAGE, status.HTTP_200_OK
        return ServiceUserRating.RATING_CREATE_MESSAGE, status.HTTP_201_CREATED

    def _update_rating(self) -> None:
        """
        Обновляет рейтинг автора на основе выбранной оценки (Mark) к его посту.

        Логика:
            - Если существует ранее присвоенная оценка (проверяется через existing_rating),
              старое значение рейтинга вычитается.
            - Добавляется новое значение рейтинга, соответствующее выбранной оценке (Mark), и сохраняется в базе данных.
        """

        mark = self._get_mark()
        author = self._get_author()

        if self.existing_rating:
            author.user_rating -= self.existing_rating.mark.value

        author.user_rating += mark.value
        author.save()

    def update_author_rating_with_return_message_and_status_code(self) -> tuple[str, int]:
        """
        Обновляет рейтинг пользователя (self._update_rating())
        и возвращает соответствующее сообщение и статусный код (self._get_message_and_status_code())
        """
        self._update_rating()
        message, status_code = self._get_message_and_status_code()
        return message, status_code
