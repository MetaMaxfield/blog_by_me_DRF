from django.core.mail import send_mail

from blog_by_me_DRF.settings import EMAIL_HOST_USER


def send(user_mail):
    """Отправление электронного письма при получении обратной связи через форму"""
    send_mail(
        'Запрос к администрации веб-приложения MAXFIELD.',
        'Ваш запрос зарегистрирован. Ожидайте обратную связь на данный адрес эл. почты. ',
        EMAIL_HOST_USER,
        [user_mail],
        fail_silently=False,
    )
