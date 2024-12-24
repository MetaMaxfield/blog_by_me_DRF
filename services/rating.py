from blog.models import Mark


def has_user_rated_post(received_ip, post):
    """
    Определяет устанавливал ли пользователь рейтинг к посту
    и возвращает id оценки
    """

    try:
        user_rating = Mark.objects.get(rating_mark__ip=received_ip, rating_mark__post=post).id
    except Mark.DoesNotExist:
        user_rating = None

    return user_rating
