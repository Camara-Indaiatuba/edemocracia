from collections import OrderedDict


GOVBR_STAGING = 'staging'
GOVBR_PRODUCTION = 'production'

GOVBR_ENVIRONMENT_CHOICES = (
    (GOVBR_STAGING, 'Homologacao/Teste'),
    (GOVBR_PRODUCTION, 'Producao'),
)

GOVBR_ENVIRONMENTS = {
    GOVBR_STAGING: {
        'issuer': 'https://sso.staging.acesso.gov.br/',
        'authorization_url': 'https://sso.staging.acesso.gov.br/authorize',
        'access_token_url': 'https://sso.staging.acesso.gov.br/token',
        'userinfo_url': 'https://sso.staging.acesso.gov.br/userinfo',
        'jwks_uri': 'https://sso.staging.acesso.gov.br/jwk',
    },
    GOVBR_PRODUCTION: {
        'issuer': 'https://sso.acesso.gov.br/',
        'authorization_url': 'https://sso.acesso.gov.br/authorize',
        'access_token_url': 'https://sso.acesso.gov.br/token',
        'userinfo_url': 'https://sso.acesso.gov.br/userinfo',
        'jwks_uri': 'https://sso.acesso.gov.br/jwk',
    },
}


def get_auth_config(defaults):
    return OrderedDict((
        ('LOGIN_EMAIL_ENABLED', (
            defaults['email_enabled'],
            'Permite login, cadastro e recuperacao de senha por e-mail.',
            bool,
        )),
        ('LOGIN_GOOGLE_ENABLED', (
            defaults['google_enabled'],
            'Permite login e cadastro com conta Google.',
            bool,
        )),
        ('LOGIN_GOOGLE_OAUTH2_KEY', (
            defaults['google_key'],
            'Client ID do OAuth Google.',
            str,
        )),
        ('LOGIN_GOOGLE_OAUTH2_SECRET', (
            defaults['google_secret'],
            'Client secret do OAuth Google.',
            'secret_text',
        )),
        ('LOGIN_GOVBR_ENABLED', (
            defaults['govbr_enabled'],
            'Permite login e cadastro com conta Gov.br.',
            bool,
        )),
        ('LOGIN_GOVBR_ENVIRONMENT', (
            defaults['govbr_environment'],
            'Ambiente Gov.br usado na autenticacao.',
            'govbr_environment_choice',
        )),
        ('LOGIN_GOVBR_CLIENT_ID', (
            defaults['govbr_client_id'],
            'Client ID emitido pelo Login Unico Gov.br.',
            str,
        )),
        ('LOGIN_GOVBR_CLIENT_SECRET', (
            defaults['govbr_client_secret'],
            'Client secret emitido pelo Login Unico Gov.br.',
            'secret_text',
        )),
        ('LOGIN_EMAIL_HOST', (
            defaults['email_host'],
            'Servidor SMTP usado para enviar ativacao de cadastro e recuperacao de senha.',
            str,
        )),
        ('LOGIN_EMAIL_PORT', (
            defaults['email_port'],
            'Porta SMTP.',
            int,
        )),
        ('LOGIN_EMAIL_HOST_USER', (
            defaults['email_host_user'],
            'Usuario SMTP.',
            str,
        )),
        ('LOGIN_EMAIL_HOST_PASSWORD', (
            defaults['email_host_password'],
            'Senha SMTP.',
            'secret_text',
        )),
        ('LOGIN_EMAIL_USE_TLS', (
            defaults['email_use_tls'],
            'Usar TLS no SMTP.',
            bool,
        )),
        ('LOGIN_EMAIL_USE_SSL', (
            defaults['email_use_ssl'],
            'Usar SSL direto no SMTP.',
            bool,
        )),
        ('LOGIN_DEFAULT_FROM_EMAIL', (
            defaults['default_from_email'],
            'Remetente padrao dos e-mails do sistema.',
            str,
        )),
        ('LOGIN_RECAPTCHA_ENABLED', (
            defaults['recaptcha_enabled'],
            'Exige reCAPTCHA no cadastro por e-mail.',
            bool,
        )),
        ('LOGIN_RECAPTCHA_SITE_KEY', (
            defaults['recaptcha_site_key'],
            'Chave publica do reCAPTCHA v2.',
            str,
        )),
        ('LOGIN_RECAPTCHA_PRIVATE_KEY', (
            defaults['recaptcha_private_key'],
            'Chave secreta do reCAPTCHA v2.',
            'secret_text',
        )),
    ))


def get_auth_fieldsets():
    return OrderedDict((
        ('Login - Formas de acesso', (
            'LOGIN_EMAIL_ENABLED',
            'LOGIN_GOOGLE_ENABLED',
            'LOGIN_GOVBR_ENABLED',
        )),
        ('Login com Google', (
            'LOGIN_GOOGLE_OAUTH2_KEY',
            'LOGIN_GOOGLE_OAUTH2_SECRET',
        )),
        ('Login com Gov.br', (
            'LOGIN_GOVBR_ENVIRONMENT',
            'LOGIN_GOVBR_CLIENT_ID',
            'LOGIN_GOVBR_CLIENT_SECRET',
        )),
        ('Login por e-mail - SMTP', (
            'LOGIN_EMAIL_HOST',
            'LOGIN_EMAIL_PORT',
            'LOGIN_EMAIL_HOST_USER',
            'LOGIN_EMAIL_HOST_PASSWORD',
            'LOGIN_EMAIL_USE_TLS',
            'LOGIN_EMAIL_USE_SSL',
            'LOGIN_DEFAULT_FROM_EMAIL',
        )),
        ('Login por e-mail - reCAPTCHA', (
            'LOGIN_RECAPTCHA_ENABLED',
            'LOGIN_RECAPTCHA_SITE_KEY',
            'LOGIN_RECAPTCHA_PRIVATE_KEY',
        )),
    ))


def _get_config_value(name, fallback=None):
    try:
        from constance import config
        return getattr(config, name)
    except Exception:
        return fallback


def is_email_login_enabled():
    return bool(_get_config_value('LOGIN_EMAIL_ENABLED', True))


def get_google_credentials():
    return (
        _get_config_value('LOGIN_GOOGLE_OAUTH2_KEY', '') or '',
        _get_config_value('LOGIN_GOOGLE_OAUTH2_SECRET', '') or '',
    )


def is_google_login_enabled():
    enabled = bool(_get_config_value('LOGIN_GOOGLE_ENABLED', False))
    key, secret = get_google_credentials()
    return bool(enabled and key and secret)


def get_govbr_environment_name():
    environment = _get_config_value('LOGIN_GOVBR_ENVIRONMENT', GOVBR_STAGING)
    if environment not in GOVBR_ENVIRONMENTS:
        return GOVBR_STAGING
    return environment


def get_govbr_environment():
    return GOVBR_ENVIRONMENTS[get_govbr_environment_name()]


def get_govbr_credentials():
    return (
        _get_config_value('LOGIN_GOVBR_CLIENT_ID', '') or '',
        _get_config_value('LOGIN_GOVBR_CLIENT_SECRET', '') or '',
    )


def is_govbr_login_enabled():
    enabled = bool(_get_config_value('LOGIN_GOVBR_ENABLED', False))
    client_id, client_secret = get_govbr_credentials()
    return bool(enabled and client_id and client_secret)


def get_recaptcha_keys():
    return (
        _get_config_value('LOGIN_RECAPTCHA_SITE_KEY', '') or '',
        _get_config_value('LOGIN_RECAPTCHA_PRIVATE_KEY', '') or '',
    )


def is_recaptcha_enabled():
    enabled = bool(_get_config_value('LOGIN_RECAPTCHA_ENABLED', False))
    site_key, private_key = get_recaptcha_keys()
    return bool(enabled and site_key and private_key)


def get_smtp_config():
    return {
        'host': _get_config_value('LOGIN_EMAIL_HOST', '') or '',
        'port': int(_get_config_value('LOGIN_EMAIL_PORT', 587) or 587),
        'username': _get_config_value('LOGIN_EMAIL_HOST_USER', '') or '',
        'password': _get_config_value('LOGIN_EMAIL_HOST_PASSWORD', '') or '',
        'use_tls': bool(_get_config_value('LOGIN_EMAIL_USE_TLS', True)),
        'use_ssl': bool(_get_config_value('LOGIN_EMAIL_USE_SSL', False)),
        'default_from_email': (
            _get_config_value('LOGIN_DEFAULT_FROM_EMAIL', '') or ''
        ),
    }
