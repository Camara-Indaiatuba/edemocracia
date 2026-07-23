from apps.core.utils import get_user_data
import logging
import requests
import json


logger = logging.getLogger(__name__)


def module_api_request(method, url, module_name, **kwargs):
    try:
        return requests.request(method, url, timeout=10, **kwargs)
    except requests.RequestException:
        logger.warning(
            'Could not synchronize data with %s; module unavailable.',
            module_name,
        )
        return None


def default_login(user, request, app_config):

    headers = {'Auth-User': user.username,
               'Remote-User-Data': json.dumps(get_user_data(user))}
    session = requests.Session()
    current_cookie = request.COOKIES.get(app_config.cookie_name)
    if current_cookie:
        session.cookies.set(app_config.cookie_name, current_cookie)

    try:
        response = session.get(app_config.upstream, headers=headers, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code == 200:
        session_cookie = (
            response.cookies.get(app_config.cookie_name) or
            session.cookies.get(app_config.cookie_name)
        )
        if session_cookie:
            request.set_cookies[app_config.cookie_name] = session_cookie
            return session_cookie

    return None
