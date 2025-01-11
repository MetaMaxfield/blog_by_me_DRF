from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import ValidationError

from blog.models import Mark, Post, Rating
from users.models import User


def has_user_rated_post(received_ip: str, post: Post) -> int | None:
    """
    Определяет устанавливал ли пользователь рейтинг к посту
    и возвращает id оценки
    """
    try:
        user_rating = Mark.objects.get(rating_mark__ip=received_ip, rating_mark__post=post).id
    except Mark.DoesNotExist:
        user_rating = None
    return user_rating


class ServiceUserRating:
    """
    Класс для управления рейтингом автора user_rating на основе оценки (Mark) для поста.

    Взаимодействие с объектом класса осуществляется через
    existing_rating или update_author_rating_with_return_message_and_status_code()
    """

    RATING_UPDATE_MESSAGE = _('Рейтинг успешно обновлен.')
    RATING_CREATE_MESSAGE = _('Рейтинг успешно добавлен.')

    def __init__(self, ip: str, post_id: int, mark_id: int) -> None:
        """
        Инициализация

        Атрибуты объекта:
        self.ip: Сохраняет IP-адрес оценивающего пользователя.
        self.post_id: Сохраняет идентификатор поста.
        self.mark_id: Сохраняет идентификатор оценки.
        self._existing_rating: Внутренний атрибут, который может иметь три значения:
            - False: Запрос к базе данных на получение рейтинга ещё не выполнялся.
            - Rating: Экземпляр модели Rating, если рейтинг найден в базе данных.
            - None: Если рейтинг в базе данных не найден.
        """
        self.ip = ip
        self.post_id = post_id
        self.mark_id = mark_id

        self._existing_rating = False

    @property
    def existing_rating(self) -> Rating | None:
        """
        Применяется как атрибут (используйте .existing_rating).

        Возвращает текущий рейтинг пользователя к посту,
        если он существует в базе данных. В противном случае возвращает None.

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
            try:
                self._existing_rating = Rating.objects.get(ip=self.ip, post=self.post_id)

            except Rating.DoesNotExist:
                self._existing_rating = None

        return self._existing_rating

    def _get_mark(self) -> Mark:
        """
        Возвращает объект оценки (Mark) по указанному ID.
        Если оценка не найдена, вызывает исключение ValidationError
        """
        try:
            mark = Mark.objects.get(id=self.mark_id)
            return mark
        except Mark.DoesNotExist:
            raise ValidationError({'detail': _('Оценка с указанным id не найдена.')})

    def _get_author(self) -> User:
        """
        Возвращает объект автора (User) по указанному ID.
        Если автор не найден, вызывает исключение ValidationError
        """
        try:
            author = User.objects.get(post_author__id=self.post_id)
            return author
        except User.DoesNotExist:
            raise ValidationError({'detail': _('Пользователь, связанный с указанным id поста, не найден.')})

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
