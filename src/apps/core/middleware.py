
from django.conf import settings


class CookieHandler:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.delete_cookies = []
        request.set_cookies = {}
        response = self.get_response(request)

        for name, value in request.set_cookies.items():
            response.set_cookie(
                name, value,
                secure=getattr(settings, 'SESSION_COOKIE_SECURE', False),
                httponly=True)

        for name in request.delete_cookies:
            response.delete_cookie(name)

        return response
