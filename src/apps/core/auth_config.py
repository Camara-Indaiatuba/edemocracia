from collections import OrderedDict


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
    ))


def get_auth_fieldsets():
    return OrderedDict((
        ('Login - Formas de acesso', (
            'LOGIN_EMAIL_ENABLED',
            'LOGIN_GOOGLE_ENABLED',
        )),
        ('Login com Google', (
            'LOGIN_GOOGLE_OAUTH2_KEY',
            'LOGIN_GOOGLE_OAUTH2_SECRET',
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
