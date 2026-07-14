from collections import OrderedDict


def get_site_config(defaults):
    return OrderedDict((
        ('PORTAL_SITE_NAME', (
            defaults['site_name'],
            'Nome da instituicao exibido no portal.',
            str,
        )),
        ('PORTAL_SITE_LOGO', (
            defaults['site_logo'],
            'Caminho do brasao ou logotipo principal.',
            str,
        )),
        ('PORTAL_LOGO_TEXT_LINE', (
            defaults['logo_text_line'],
            'Primeira linha do texto ao lado do brasao.',
            str,
        )),
        ('PORTAL_LOGO_TEXT_CITY', (
            defaults['logo_text_city'],
            'Segunda linha do texto ao lado do brasao.',
            str,
        )),
    ))


def get_site_fieldsets():
    return OrderedDict((
        ('Identidade do portal', (
            'PORTAL_SITE_NAME',
            'PORTAL_SITE_LOGO',
            'PORTAL_LOGO_TEXT_LINE',
            'PORTAL_LOGO_TEXT_CITY',
        )),
    ))


def _get_config_value(name, fallback=None):
    try:
        from constance import config
        return getattr(config, name)
    except Exception:
        return fallback


def get_site_identity():
    from django.conf import settings

    return {
        'site_name': _get_config_value('PORTAL_SITE_NAME',
                                      settings.SITE_NAME),
        'site_logo': _get_config_value('PORTAL_SITE_LOGO',
                                      settings.SITE_LOGO),
        'site_logo_text_line': _get_config_value(
            'PORTAL_LOGO_TEXT_LINE',
            settings.SITE_LOGO_TEXT_LINE,
        ),
        'site_logo_text_city': _get_config_value(
            'PORTAL_LOGO_TEXT_CITY',
            settings.SITE_LOGO_TEXT_CITY,
        ),
    }
