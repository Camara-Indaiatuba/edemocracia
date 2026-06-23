from apps.core.views import EdemProxyView
from django.conf import settings
from django.contrib.auth import logout as auth_logout
import re


GLOBAL_AUTH_COOKIES = (
    settings.SESSION_COOKIE_NAME,
    'audiencias_session',
    'wikilegis_session',
    '_forum_session',
    '_t',
)

SCRIPT_NONCE_RE = re.compile(r"script-src[^;]*'nonce-([^']+)'")
INJECTED_SCRIPT_RE = re.compile(
    r'(<script\b(?![^>]*\bnonce=)'
    r'(?=[^>]*\bsrc="(?:/static/|https://www\.google\.com/recaptcha/))'
    r'[^>]*>)'
)


class DiscourseProxyView(EdemProxyView):
    upstream = settings.DISCOURSE_UPSTREAM
    diazo_theme_template = 'diazo-discourse.html'

    def _allow_injected_scripts(self, response):
        csp = response.get('Content-Security-Policy', '')
        nonce_match = SCRIPT_NONCE_RE.search(csp)
        content_type = response.get('Content-Type', '')

        if not nonce_match or 'text/html' not in content_type:
            return response

        try:
            content = response.content.decode(response.charset)
        except AttributeError:
            return response

        nonce = nonce_match.group(1)

        def add_nonce(match):
            tag = match.group(1)
            return tag[:-1] + ' nonce="{}">'.format(nonce)

        updated_content = INJECTED_SCRIPT_RE.sub(add_nonce, content)

        if updated_content != content:
            response.content = updated_content.encode(response.charset)
            if response.has_header('Content-Length'):
                response['Content-Length'] = str(len(response.content))

        return response

    def dispatch(self, request, *args, **kwargs):
        is_discourse_logout = (
            request.method == 'DELETE' and
            request.path.startswith('/expressao/session/')
        )

        response = super().dispatch(request, *args, **kwargs)
        response = self._allow_injected_scripts(response)

        if is_discourse_logout and response.status_code < 400:
            if request.user.is_authenticated:
                auth_logout(request)

            for cookie_name in GLOBAL_AUTH_COOKIES:
                response.delete_cookie(cookie_name)

        return response
