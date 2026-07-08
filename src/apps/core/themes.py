from urllib.parse import quote


THEME_ORIGINAL = 'original'
THEME_BLUE_WHITE_RED = 'blue_white_red'
THEME_BLUE_GREEN = 'blue_green'
THEME_WHITE_RED = 'white_red'
THEME_BLUE_RED_YELLOW = 'blue_red_yellow'

THEME_CHOICES = (
    (THEME_ORIGINAL, 'Tema 1 - Original'),
    (THEME_BLUE_WHITE_RED, 'Tema 2 - Azul, branco e vermelho'),
    (THEME_BLUE_GREEN, 'Tema 3 - Azul e verde'),
    (THEME_WHITE_RED, 'Tema 4 - Branco e vermelho'),
    (THEME_BLUE_RED_YELLOW, 'Tema 5 - Azul, vermelho e amarelo'),
)

THEME_PRESETS = {
    THEME_BLUE_WHITE_RED: {
        'primary': '#005ca7',
        'primary_dark': '#003d73',
        'secondary': '#d71920',
        'accent': '#ffffff',
        'link': '#ffb3b8',
        'surface': '#ffffff',
        'surface_alt': '#f2f7fc',
        'text': '#24465f',
        'on_primary': '#ffffff',
        'on_secondary': '#ffffff',
    },
    THEME_BLUE_GREEN: {
        'primary': '#075985',
        'primary_dark': '#064e3b',
        'secondary': '#16a34a',
        'accent': '#7dd3fc',
        'link': '#86efac',
        'surface': '#ffffff',
        'surface_alt': '#eef9f5',
        'text': '#12384d',
        'on_primary': '#ffffff',
        'on_secondary': '#ffffff',
    },
    THEME_WHITE_RED: {
        'primary': '#ffffff',
        'primary_dark': '#f2f2f2',
        'secondary': '#b91c1c',
        'accent': '#ef4444',
        'link': '#b91c1c',
        'surface': '#ffffff',
        'surface_alt': '#fff5f5',
        'text': '#5f1515',
        'on_primary': '#7f1d1d',
        'on_secondary': '#ffffff',
    },
    THEME_BLUE_RED_YELLOW: {
        'primary': '#123c7c',
        'primary_dark': '#09244d',
        'secondary': '#d62828',
        'accent': '#f6c445',
        'link': '#f6c445',
        'surface': '#ffffff',
        'surface_alt': '#f4f7fb',
        'text': '#173451',
        'on_primary': '#ffffff',
        'on_secondary': '#ffffff',
    },
}

THEME_ALIASES = {
    'indaiatuba': THEME_BLUE_WHITE_RED,
}

THEME_COLOR_FIELDS = (
    ('primary', 'COR_PRINCIPAL', 'cor principal'),
    ('primary_dark', 'COR_PRINCIPAL_ESCURA', 'cor principal escura'),
    ('secondary', 'COR_SECUNDARIA', 'cor secundaria'),
    ('accent', 'COR_DESTAQUE', 'cor de destaque'),
    ('link', 'COR_LINK', 'cor de links e textos destacados'),
    ('surface', 'COR_FUNDO_CLARO', 'fundo claro'),
    ('surface_alt', 'COR_FUNDO_ALTERNATIVO', 'fundo alternativo'),
    ('text', 'COR_TEXTO', 'texto principal'),
    ('on_primary', 'COR_TEXTO_SOBRE_PRINCIPAL', 'texto sobre a cor principal'),
    ('on_secondary', 'COR_TEXTO_SOBRE_DESTAQUE', 'texto sobre cores de destaque'),
)

THEME_COLOR_CONFIG_PREFIXES = {
    THEME_BLUE_WHITE_RED: 'TEMA_2',
    THEME_BLUE_GREEN: 'TEMA_3',
    THEME_WHITE_RED: 'TEMA_4',
    THEME_BLUE_RED_YELLOW: 'TEMA_5',
}

THEME_COLOR_CONFIG = {
    theme: {
        key: '{}_{}'.format(prefix, suffix)
        for key, suffix, _label in THEME_COLOR_FIELDS
    }
    for theme, prefix in THEME_COLOR_CONFIG_PREFIXES.items()
}

LEFT_LEAK_SVG = (
    '<svg style="isolation:isolate" version="1.1" viewBox="0 0 128 320" '
    'xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="a"><rect '
    'width="128" height="320"/></clipPath></defs><g clip-path="url(#a)">'
    '<path d="m80 0c-53.81 74.25-80 156.5-80 232 0 41.3 4.25 69.2 '
    '8 88h48l14-120 58-200h-48z" fill="{outer}"/>'
    '<path d="m89.29 124.3l38.71-124.3h-32c-19 23.43-45.2 94.29-47.6 '
    '156.6q-2.4 62.4 21.6 82.4l19.29-114.7z" fill="{middle}"/>'
    '<path d="m128 0c-64.7 77.75-76.09 147.4-79.89 200-2.86 39.7.83 '
    '88.2 6.66 120h73.23v-320z" fill="{inner}"/></g></svg>'
)

TOP_LEAK_SVG = (
    '<svg style="isolation:isolate" xmlns="http://www.w3.org/2000/svg" '
    'version="1.1" viewBox="0 0 480 80"><defs><clipPath id="a"><rect '
    'width="480" height="80"/></clipPath></defs><g fill-rule="evenodd" '
    'clip-path="url(#a)">'
    '<path fill="{outer}" d="m480 48c-92.9-72.5-347.1-52.55-480-8v40h480v-32z"/>'
    '<path fill="{middle}" d="m480 32c-150-36.24-347.4-4.58-480 40v8h480v-48z"/>'
    '<path fill="{inner}" d="m423.5 32.86c-151.7-14.87-305.4 '
    '6.44-423.5 46.14v1h480v-40q-38-5.33-56.5-7.14z"/></g></svg>'
)


def _labels():
    return dict(THEME_CHOICES)


def _valid_color(value, fallback):
    if isinstance(value, str) and len(value) == 7 and value.startswith('#'):
        hexdigits = value[1:]
        if all(char in '0123456789abcdefABCDEF' for char in hexdigits):
            return value.lower()
    return fallback


def _configured_colors(config, selected_theme):
    defaults = THEME_PRESETS[selected_theme]
    colors = {}

    for key, _suffix, _label in THEME_COLOR_FIELDS:
        config_name = THEME_COLOR_CONFIG[selected_theme][key]
        colors[key] = _valid_color(getattr(config, config_name, defaults[key]), defaults[key])

    return colors


def _svg_data_uri(svg):
    return 'data:image/svg+xml,{}'.format(quote(svg, safe='/,:;=-_.()'))


def _theme_assets(colors):
    svg_colors = {
        'outer': colors['secondary'],
        'middle': colors['accent'],
        'inner': colors['primary_dark'],
    }

    return {
        'left_leak': _svg_data_uri(LEFT_LEAK_SVG.format(**svg_colors)),
        'top_leak': _svg_data_uri(TOP_LEAK_SVG.format(**svg_colors)),
    }


def get_theme_color_config():
    labels = _labels()
    theme_config = {}

    for theme, color_config in THEME_COLOR_CONFIG.items():
        for key, _suffix, color_label in THEME_COLOR_FIELDS:
            config_name = color_config[key]
            theme_config[config_name] = (
                THEME_PRESETS[theme][key],
                '{}: {}.'.format(labels[theme], color_label),
                'theme_color',
            )

    return theme_config


def get_theme_color_fieldsets():
    labels = _labels()
    fieldsets = {
        'Tema visual': (
            'TEMA_VISUAL',
        ),
    }

    for theme, color_config in THEME_COLOR_CONFIG.items():
        fieldsets['Cores - {}'.format(labels[theme])] = tuple(
            color_config[key]
            for key, _suffix, _label in THEME_COLOR_FIELDS
        )

    return fieldsets


def reset_config_colors(config, selected_theme):
    if selected_theme not in THEME_COLOR_CONFIG:
        return False

    for key, value in THEME_PRESETS[selected_theme].items():
        setattr(config, THEME_COLOR_CONFIG[selected_theme][key], value)

    return True


def get_active_theme():
    from constance import config

    selected_theme = getattr(config, 'TEMA_VISUAL', THEME_ORIGINAL)
    selected_theme = THEME_ALIASES.get(selected_theme, selected_theme)
    labels = _labels()

    if selected_theme not in THEME_PRESETS:
        return {
            'enabled': False,
            'slug': THEME_ORIGINAL,
            'label': labels[THEME_ORIGINAL],
            'colors': {},
        }

    colors = _configured_colors(config, selected_theme)

    return {
        'enabled': True,
        'slug': selected_theme,
        'label': labels.get(selected_theme, selected_theme),
        'colors': colors,
        'assets': _theme_assets(colors),
    }
