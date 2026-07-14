from collections import OrderedDict


MODULES = OrderedDict((
    ('AUDIENCIAS', {
        'label': 'Audiências',
        'field': 'MODULE_AUDIENCIAS_ENABLED',
        'settings_field': 'AUDIENCIAS_ENABLED',
        'path_prefix': '/audiencias/',
    }),
    ('WIKILEGIS', {
        'label': 'Wikilegis',
        'field': 'MODULE_WIKILEGIS_ENABLED',
        'settings_field': 'WIKILEGIS_ENABLED',
        'path_prefix': '/wikilegis/',
    }),
    ('DISCOURSE', {
        'label': 'Expressão',
        'field': 'MODULE_DISCOURSE_ENABLED',
        'settings_field': 'DISCOURSE_ENABLED',
        'path_prefix': '/expressao/',
    }),
))


def get_module_config(defaults):
    return OrderedDict(
        (
            data['field'],
            (
                defaults.get(data['settings_field'], True),
                'Exibir e permitir acesso ao modulo {}.'.format(data['label']),
                bool,
            ),
        )
        for data in MODULES.values()
    )


def get_module_fieldsets():
    return OrderedDict((
        ('Módulos exibidos', tuple(
            data['field'] for data in MODULES.values()
        )),
    ))


def _get_config_value(name, fallback=None):
    try:
        from constance import config
        return getattr(config, name)
    except Exception:
        return fallback


def is_module_enabled(module_name):
    from django.conf import settings

    data = MODULES[module_name]
    infrastructure_enabled = bool(
        getattr(settings, data['settings_field'], False)
    )
    admin_enabled = bool(
        _get_config_value(data['field'], infrastructure_enabled)
    )
    return bool(infrastructure_enabled and admin_enabled)


def is_audiencias_enabled():
    return is_module_enabled('AUDIENCIAS')


def is_wikilegis_enabled():
    return is_module_enabled('WIKILEGIS')


def is_discourse_enabled():
    return is_module_enabled('DISCOURSE')


def module_from_path(path):
    normalized_path = path if path.endswith('/') else path + '/'
    for module_name, data in MODULES.items():
        if normalized_path.startswith(data['path_prefix']):
            return module_name
    return None
