from decouple import Csv, config

from .settings import *  # noqa: F403


CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=Csv(),
)
SESSION_COOKIE_SECURE = config(
    'SESSION_COOKIE_SECURE',
    default=False,
    cast=bool,
)
CSRF_COOKIE_SECURE = config(
    'CSRF_COOKIE_SECURE',
    default=False,
    cast=bool,
)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MIDDLEWARE = [
    (
        'audiencias_publicas.permission_preserving_auth.'
        'PermissionPreservingAudienciasRemoteUser'
        if middleware == 'apps.accounts.middlewares.AudienciasRemoteUser'
        else middleware
    )
    for middleware in MIDDLEWARE  # noqa: F405
]

AUTHENTICATION_BACKENDS = [
    (
        'audiencias_publicas.permission_preserving_auth.'
        'PermissionPreservingAudienciasAuthBackend'
        if backend == 'apps.accounts.backends.AudienciasAuthBackend'
        else backend
    )
    for backend in AUTHENTICATION_BACKENDS  # noqa: F405
]
