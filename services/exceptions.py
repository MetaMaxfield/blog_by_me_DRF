from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_204_NO_CONTENT


class NoContent(APIException):
    """
    Исключение для обработки отсутствия результатов поиска.

    Используется для упрощения кода в представлениях
    (вызов ошибки в сервисном слое автоматически формирует ответ с кодом 204 (No Content) в представлении)
    """

    status_code = HTTP_204_NO_CONTENT
    default_detail = 'Запрос выполнен успешно, но содержимое отсутствует.'
    default_code = 'no_content'
