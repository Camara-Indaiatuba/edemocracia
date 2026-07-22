from django.conf import settings

from .auth_config import (
    get_recaptcha_keys,
    is_email_login_enabled,
    is_govbr_login_enabled,
    is_google_login_enabled,
    is_recaptcha_enabled,
)
from .module_config import (
    is_audiencias_enabled,
    is_discourse_enabled,
    is_wikilegis_enabled,
)
from .site_config import get_site_identity
from .themes import get_active_theme


def settings_variables(request):
    recaptcha_site_key, _ = get_recaptcha_keys()
    return {
        'SITE_URL': settings.SITE_URL,
        'RECAPTCHA_ENABLED': is_recaptcha_enabled(),
        'RECAPTCHA_SITE_KEY': recaptcha_site_key,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'OLARK_ID': settings.OLARK_ID,
        'WIKILEGIS_ENABLED': is_wikilegis_enabled(),
        'PAUTAS_ENABLED': settings.PAUTAS_ENABLED,
        'DISCOURSE_ENABLED': is_discourse_enabled(),
        'AUDIENCIAS_ENABLED': is_audiencias_enabled(),
        'EMAIL_LOGIN_ENABLED': is_email_login_enabled(),
        'GOOGLE_LOGIN_ENABLED': is_google_login_enabled(),
        'GOVBR_LOGIN_ENABLED': is_govbr_login_enabled(),
        'FACEBOOK_LOGIN_ENABLED': bool(settings.SOCIAL_AUTH_FACEBOOK_KEY
                                       and settings.SOCIAL_AUTH_FACEBOOK_SECRET),
    }


def home_customization(request):
    return get_site_identity()


def theme_customization(request):
    return {
        'active_theme': get_active_theme(),
    }
