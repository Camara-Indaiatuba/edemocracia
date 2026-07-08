from django.conf import settings

from .auth_config import is_email_login_enabled, is_google_login_enabled
from .themes import get_active_theme


def settings_variables(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'OLARK_ID': settings.OLARK_ID,
        'WIKILEGIS_ENABLED': settings.WIKILEGIS_ENABLED,
        'PAUTAS_ENABLED': settings.PAUTAS_ENABLED,
        'DISCOURSE_ENABLED': settings.DISCOURSE_ENABLED,
        'AUDIENCIAS_ENABLED': settings.AUDIENCIAS_ENABLED,
        'EMAIL_LOGIN_ENABLED': is_email_login_enabled(),
        'GOOGLE_LOGIN_ENABLED': is_google_login_enabled(),
        'FACEBOOK_LOGIN_ENABLED': bool(settings.SOCIAL_AUTH_FACEBOOK_KEY
                                       and settings.SOCIAL_AUTH_FACEBOOK_SECRET),
    }


def home_customization(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_logo': settings.SITE_LOGO,
        'site_logo_text_line': settings.SITE_LOGO_TEXT_LINE,
        'site_logo_text_city': settings.SITE_LOGO_TEXT_CITY,
    }


def theme_customization(request):
    return {
        'active_theme': get_active_theme(),
    }
