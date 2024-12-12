from django.conf import settings
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class ForceInRussian(MiddlewareMixin):
    """
    Промежуточное программное обеспечение, которое
    установливает языковой файл cookie в запросе
    на русский язык для панели администратора по умолчанию
    """

    def process_request(self, request: HttpRequest) -> None:
        if request.path.startswith('/admin'):
            request.COOKIES[settings.LANGUAGE_COOKIE_NAME] = 'ru'
