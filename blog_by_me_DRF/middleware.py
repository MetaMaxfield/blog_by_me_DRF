from django.conf import settings
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from blog_by_me_DRF.settings import LANGUAGES


class ForceInRussian(MiddlewareMixin):
    """
    Промежуточное программное обеспечение, которое
    установливает языковой файл cookie в запросе
    на русский язык для панели администратора по умолчанию
    """

    def process_request(self, request: HttpRequest) -> None:
        if request.path.startswith('/admin'):
            request.COOKIES[settings.LANGUAGE_COOKIE_NAME] = LANGUAGES[0][0]
