import hashlib

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from social_core.backends.google import GoogleOAuth2
from social_core.backends.open_id_connect import OpenIdConnectAuth

from apps.core.auth_config import (
    get_google_credentials,
    get_govbr_credentials,
    get_govbr_environment,
    is_govbr_login_enabled,
)


class ConfigurableGoogleOAuth2(GoogleOAuth2):
    def get_key_and_secret(self):
        return get_google_credentials()


class ConfigurableGovBrOpenIDConnect(OpenIdConnectAuth):
    name = 'govbr'
    DEFAULT_SCOPE = [
        'openid',
        'email',
        'profile',
        'govbr_confiabilidades',
        'govbr_confiabilidades_idtoken',
    ]
    TOKEN_ENDPOINT_AUTH_METHOD = 'client_secret_basic'
    DEFAULT_USE_PKCE = True
    PKCE_DEFAULT_CODE_CHALLENGE_METHOD = 'S256'
    USERNAME_KEY = 'preferred_username'
    EMAIL_KEY = 'email'
    FULLNAME_KEY = 'name'
    EXTRA_DATA = [
        'id_token',
        ('sub', 'id'),
        'preferred_username',
        'email_verified',
        'phone_number_verified',
        'reliability_info',
    ]

    def get_key_and_secret(self):
        return get_govbr_credentials()

    def auth_url(self):
        if not is_govbr_login_enabled():
            return '/'
        return super().auth_url()

    def _environment_setting(self, name):
        return get_govbr_environment()[name]

    def authorization_url(self):
        return self._environment_setting('authorization_url')

    def access_token_url(self):
        return self._environment_setting('access_token_url')

    def id_token_issuer(self):
        return self._environment_setting('issuer')

    def userinfo_url(self):
        return self._environment_setting('userinfo_url')

    def jwks_uri(self):
        return self._environment_setting('jwks_uri')

    def get_user_details(self, response):
        details = super().get_user_details(response)
        identifier = details.get('username') or response.get('sub') or ''
        email = details.get('email') or ''
        fullname = details.get('fullname') or response.get('name') or ''
        name_parts = fullname.split(None, 1)

        details['username'] = self._build_username(identifier, email, fullname)
        details['fullname'] = fullname
        if not details.get('first_name'):
            details['first_name'] = name_parts[0] if name_parts else ''
        if not details.get('last_name'):
            details['last_name'] = name_parts[1] if len(name_parts) > 1 else ''

        return details

    @staticmethod
    def _build_username(identifier, email, fullname):
        if email:
            base = email.split('@', 1)[0]
        elif fullname:
            base = fullname
        else:
            base = 'govbr'

        slug = slugify(base)[:30] or 'govbr'
        if not identifier:
            return slug

        digest = hashlib.sha256(identifier.encode('utf-8')).hexdigest()[:8]
        return '{}-{}'.format(slug[:21], digest)


class AuthenticationEmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        username = username or kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
