from urllib.parse import parse_qs, urlparse

import requests
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from pydiscourse.sso import sso_validate, sso_redirect_url

from apps.core.module_config import is_discourse_enabled


@receiver(user_logged_in)
def discourse_login(sender, user, request, **kwargs):
    if not is_discourse_enabled():
        return

    upstream = settings.DISCOURSE_UPSTREAM
    upstream = upstream[:-1] if upstream[-1] == '/' else upstream

    session = requests.Session()
    try:
        response = session.get(
            upstream + '/session/sso',
            allow_redirects=False,
            timeout=10,
        )
    except requests.RequestException:
        return

    if response.status_code == 302:
        location = response.headers['Location']

        query = parse_qs(urlparse(location).query)
        payload = query.get('sso', [None])[0]
        signature = query.get('sig', [None])[0]
        if not payload or not signature:
            return

        secret = settings.DISCOURSE_SSO_SECRET

        try:
            nonce = sso_validate(payload, signature, secret)
            url = sso_redirect_url(nonce, secret, user.email, user.id,
                                   user.username,
                                   name=user.get_full_name())
            response = session.get(upstream + url, allow_redirects=False,
                                   timeout=10)
        except (requests.RequestException, ValueError):
            return

        t_cookie = response.cookies.get('_t') or session.cookies.get('_t')

        if t_cookie:
            request.set_cookies['_t'] = t_cookie


@receiver(user_logged_out)
def discourse_logout(sender, user, request, **kwargs):
    request.delete_cookies.append('_forum_session')
    request.delete_cookies.append('_t')
