from django.conf import settings


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
        'GOOGLE_LOGIN_ENABLED': bool(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
                                     and settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET),
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
