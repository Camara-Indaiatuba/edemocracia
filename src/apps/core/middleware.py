
from django.conf import settings
from django.http import HttpResponseNotFound

from apps.core.module_config import is_module_enabled, module_from_path


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


class ModuleVisibilityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        module_name = module_from_path(request.path)
        if module_name and not is_module_enabled(module_name):
            return HttpResponseNotFound('Modulo desativado.')

        return self.get_response(request)
