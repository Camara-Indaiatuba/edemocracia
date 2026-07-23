from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import SimpleTestCase
from social_core.backends.open_id_connect import OpenIdConnectAuth

from apps.accounts.backends import ConfigurableGovBrOpenIDConnect
from apps.accounts.pipeline import associate_by_verified_email
from apps.accounts.views import ajax_sync_sessions
from apps.audiencias.apps import AudienciasConfig
from apps.core.auth_config import (
    GOVBR_STAGING,
    get_govbr_environment_name,
    is_govbr_login_enabled,
)
from apps.wikilegis.apps import WikilegisConfig


class GovBrBackendTests(SimpleTestCase):
    @patch.object(OpenIdConnectAuth, 'get_user_details')
    def test_name_falls_back_to_fullname_when_separate_claims_are_missing(
            self, get_user_details):
        get_user_details.return_value = {
            'username': 'govbr-identifier',
            'email': 'cidadao@example.org',
            'fullname': 'Maria da Silva',
            'first_name': None,
            'last_name': None,
        }

        backend = ConfigurableGovBrOpenIDConnect()
        details = backend.get_user_details({})

        self.assertEqual(details['first_name'], 'Maria')
        self.assertEqual(details['last_name'], 'da Silva')

    @patch.object(OpenIdConnectAuth, 'get_user_details')
    def test_separate_name_claims_are_preserved(self, get_user_details):
        get_user_details.return_value = {
            'username': 'govbr-identifier',
            'email': 'cidadao@example.org',
            'fullname': 'Maria da Silva',
            'first_name': 'Maria',
            'last_name': 'Silva',
        }

        backend = ConfigurableGovBrOpenIDConnect()
        details = backend.get_user_details({})

        self.assertEqual(details['first_name'], 'Maria')
        self.assertEqual(details['last_name'], 'Silva')

    def test_username_is_deterministic_without_exposing_identifier(self):
        identifier = '12345678900'

        username = ConfigurableGovBrOpenIDConnect._build_username(
            identifier,
            'cidadao@example.org',
            'Cidadao de Teste',
        )

        self.assertEqual(username, 'cidadao-a8476735')
        self.assertNotIn(identifier, username)

    @patch('apps.accounts.pipeline.associate_by_email')
    def test_unverified_govbr_email_is_not_associated(self, associate):
        backend = SimpleNamespace(name='govbr', id_token={})

        result = associate_by_verified_email(
            backend,
            {'email': 'cidadao@example.org'},
            response={'email_verified': False},
        )

        self.assertIsNone(result)
        associate.assert_not_called()

    @patch('apps.accounts.pipeline.associate_by_email')
    def test_verified_govbr_email_can_be_associated(self, associate):
        backend = SimpleNamespace(name='govbr', id_token={})
        associate.return_value = {'user': object()}

        result = associate_by_verified_email(
            backend,
            {'email': 'cidadao@example.org'},
            response={'email_verified': True},
        )

        self.assertEqual(result, associate.return_value)
        associate.assert_called_once()


class GovBrConfigurationTests(SimpleTestCase):
    @patch('apps.core.auth_config._get_config_value', return_value='invalid')
    def test_invalid_environment_falls_back_to_staging(self, _config):
        self.assertEqual(get_govbr_environment_name(), GOVBR_STAGING)

    @patch('apps.core.auth_config.get_govbr_credentials', return_value=('', ''))
    @patch('apps.core.auth_config._get_config_value', return_value=True)
    def test_login_requires_credentials(self, _config, _credentials):
        self.assertFalse(is_govbr_login_enabled())


class ExternalSessionSyncTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Mock(spec=get_user_model())
        self.user.is_authenticated = True

    def _request(self, cookies=None):
        request = self.factory.get('/accounts/ajax/sync-sessions/')
        request.user = self.user
        request.COOKIES = cookies or {}
        request.set_cookies = {}
        return request

    @patch('apps.accounts.views.is_discourse_enabled', return_value=False)
    @patch('apps.accounts.views.is_wikilegis_enabled', return_value=False)
    @patch('apps.accounts.views.is_audiencias_enabled', return_value=True)
    @patch('apps.accounts.views.default_login', return_value='fresh-session')
    def test_stale_audiencias_cookie_is_replaced(
            self, login, _audiencias, _wikilegis, _discourse):
        request = self._request({
            AudienciasConfig.cookie_name: 'stale-session',
        })

        response = ajax_sync_sessions(request)

        self.assertJSONEqual(
            response.content,
            {'synced': ['audiencias']},
        )
        login.assert_called_once_with(
            self.user, request, AudienciasConfig)

    @patch('apps.accounts.views.is_discourse_enabled', return_value=False)
    @patch('apps.accounts.views.is_wikilegis_enabled', return_value=True)
    @patch('apps.accounts.views.is_audiencias_enabled', return_value=False)
    @patch('apps.accounts.views.default_login', return_value='valid-session')
    def test_valid_wikilegis_cookie_does_not_trigger_reload(
            self, login, _audiencias, _wikilegis, _discourse):
        request = self._request({
            WikilegisConfig.cookie_name: 'valid-session',
        })

        response = ajax_sync_sessions(request)

        self.assertJSONEqual(response.content, {'synced': []})
        login.assert_called_once_with(
            self.user, request, WikilegisConfig)

    @patch('apps.accounts.views.is_discourse_enabled', return_value=False)
    @patch('apps.accounts.views.is_wikilegis_enabled', return_value=False)
    @patch('apps.accounts.views.is_audiencias_enabled', return_value=True)
    @patch('apps.accounts.views.default_login', return_value='new-session')
    def test_missing_audiencias_cookie_is_created(
            self, login, _audiencias, _wikilegis, _discourse):
        request = self._request()

        response = ajax_sync_sessions(request)

        self.assertJSONEqual(
            response.content,
            {'synced': ['audiencias']},
        )
        login.assert_called_once_with(
            self.user, request, AudienciasConfig)
