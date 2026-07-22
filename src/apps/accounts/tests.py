from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.accounts.backends import ConfigurableGovBrOpenIDConnect
from apps.accounts.pipeline import associate_by_verified_email
from apps.core.auth_config import (
    GOVBR_STAGING,
    get_govbr_environment_name,
    is_govbr_login_enabled,
)


class GovBrBackendTests(SimpleTestCase):
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
