from rest_framework.renderers import BrowsableAPIRenderer


class NoHTMLFormBrowsableAPIRenderer(BrowsableAPIRenderer):

    def get_rendered_html_form(self, *args, **kwargs):
        """
        Отключает рендеринг HTML-формы при тестировании POST-запросов
        через BrowsableAPIRenderer
        """
        return ""
