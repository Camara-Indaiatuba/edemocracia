from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from requests import RequestException
from requests.cookies import RequestsCookieJar

from apps.core.tasks import default_login, module_api_request


class DefaultLoginTests(SimpleTestCase):
    @patch('apps.core.tasks.get_user_data', return_value={'email': 'a@b.test'})
    @patch('apps.core.tasks.requests.Session')
    def test_existing_module_cookie_is_reused(
            self, session_class, _user_data):
        cookie_name = 'module_session'
        cookie_jar = RequestsCookieJar()
        session = session_class.return_value
        session.cookies = cookie_jar
        response = Mock()
        response.status_code = 200
        response.cookies = RequestsCookieJar()
        session.get.return_value = response
        request = SimpleNamespace(
            COOKIES={cookie_name: 'current-session'},
            set_cookies={},
        )
        app_config = SimpleNamespace(
            cookie_name=cookie_name,
            upstream='http://module/',
        )
        user = SimpleNamespace(username='cidadao')

        synced_cookie = default_login(user, request, app_config)

        self.assertEqual(synced_cookie, 'current-session')
        self.assertEqual(
            request.set_cookies[cookie_name],
            'current-session',
        )
        session.get.assert_called_once()

    @patch('apps.core.tasks.get_user_data', return_value={'email': 'a@b.test'})
    @patch('apps.core.tasks.requests.Session')
    def test_new_cookie_replaces_stale_module_cookie(
            self, session_class, _user_data):
        cookie_name = 'module_session'
        session = session_class.return_value
        session.cookies = RequestsCookieJar()
        response = Mock()
        response.status_code = 200
        response.cookies = RequestsCookieJar()
        response.cookies.set(cookie_name, 'fresh-session')
        session.get.return_value = response
        request = SimpleNamespace(
            COOKIES={cookie_name: 'stale-session'},
            set_cookies={},
        )
        app_config = SimpleNamespace(
            cookie_name=cookie_name,
            upstream='http://module/',
        )
        user = SimpleNamespace(username='cidadao')

        synced_cookie = default_login(user, request, app_config)

        self.assertEqual(synced_cookie, 'fresh-session')
        self.assertEqual(
            request.set_cookies[cookie_name],
            'fresh-session',
        )


class ModuleApiRequestTests(SimpleTestCase):
    @patch(
        'apps.core.tasks.requests.request',
        side_effect=RequestException('secret-url-must-not-be-logged'),
    )
    def test_connection_failure_is_sanitized(self, request):
        with self.assertLogs('apps.core.tasks', level='WARNING') as logs:
            response = module_api_request(
                'put',
                'http://module/api/?api_key=internal-secret',
                'Modulo',
            )

        self.assertIsNone(response)
        self.assertNotIn('internal-secret', ' '.join(logs.output))
        self.assertNotIn('secret-url-must-not-be-logged', ' '.join(logs.output))
        request.assert_called_once_with(
            'put',
            'http://module/api/?api_key=internal-secret',
            timeout=10,
        )
