from apps.core.utils import get_user_data
import requests
import json


def default_login(user, request, app_config):

    headers = {'Auth-User': user.username,
               'Remote-User-Data': json.dumps(get_user_data(user))}
    session = requests.Session()
    try:
        response = session.get(app_config.upstream, headers=headers, timeout=10)
    except requests.RequestException:
        return

    if response.status_code == 200:
        session_cookie = (
            response.cookies.get(app_config.cookie_name) or
            session.cookies.get(app_config.cookie_name)
        )
        if session_cookie:
            request.set_cookies[app_config.cookie_name] = session_cookie
