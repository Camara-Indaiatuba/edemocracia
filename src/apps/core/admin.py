from collections import OrderedDict
from contextlib import contextmanager

from constance import settings as constance_settings
from constance.admin import Config, ConstanceAdmin
from django.apps import apps
from django.conf import settings as django_settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from apps.core.auth_config import get_auth_fieldsets
from apps.core.constance_forms import LoginConstanceForm, ThemeConstanceForm
from apps.core.module_config import get_module_fieldsets
from apps.core.site_config import get_site_fieldsets
from apps.core.themes import get_theme_color_fieldsets


class ConfigMeta:
    app_label = 'core'
    concrete_model = None
    abstract = False
    swapped = False
    is_composite_pk = False

    def __init__(self, model_name, object_name, verbose_name_plural):
        self.model_name = self.module_name = model_name
        self.object_name = object_name
        self.verbose_name_plural = verbose_name_plural

    def get_ordered_objects(self):
        return False

    def get_change_permission(self):
        return 'change_{}'.format(self.model_name)

    @property
    def app_config(self):
        return apps.get_app_config(self.app_label)

    @property
    def label(self):
        return '{}.{}'.format(self.app_label, self.object_name)

    @property
    def label_lower(self):
        return '{}.{}'.format(self.app_label, self.model_name)


class ThemeSettings:
    _meta = ConfigMeta('theme_settings', 'ThemeSettings', 'Tema visual')


class LoginSettings:
    _meta = ConfigMeta('login_settings', 'LoginSettings', 'Formas de login')


class ModuleSettings:
    _meta = ConfigMeta('module_settings', 'ModuleSettings', 'Módulos')


class SiteSettings:
    _meta = ConfigMeta('site_settings', 'SiteSettings', 'Identidade do portal')


def _fieldset_fields(fieldsets):
    fields = []

    for fieldset_data in fieldsets.values():
        if isinstance(fieldset_data, dict):
            fields.extend(fieldset_data['fields'])
        else:
            fields.extend(fieldset_data)

    return fields


@contextmanager
def _constance_settings_subset(fieldsets):
    previous_config = constance_settings.CONFIG
    previous_fieldsets = constance_settings.CONFIG_FIELDSETS
    fields = _fieldset_fields(fieldsets)

    constance_settings.CONFIG = OrderedDict(
        (field, django_settings.CONSTANCE_CONFIG[field])
        for field in fields
    )
    constance_settings.CONFIG_FIELDSETS = fieldsets

    try:
        yield
    finally:
        constance_settings.CONFIG = previous_config
        constance_settings.CONFIG_FIELDSETS = previous_fieldsets


class SplitConstanceAdmin(ConstanceAdmin):
    config_fieldsets = OrderedDict()
    secret_mask = '********'

    def get_config_value(self, name, options, form, initial):
        config_value = super().get_config_value(name, options, form, initial)
        field_type = options[2] if len(options) == 3 else None

        if field_type == 'secret_text':
            config_value.update({
                'default': self.secret_mask if options[0] else '',
                'raw_default': '',
                'value': self.secret_mask if config_value.get('value') else '',
                'is_secret': True,
            })

        return config_value

    def changelist_view(self, request, extra_context=None):
        with _constance_settings_subset(self.config_fieldsets):
            return super().changelist_view(request, extra_context)


class ThemeSettingsAdmin(SplitConstanceAdmin):
    change_list_form = ThemeConstanceForm
    config_fieldsets = get_theme_color_fieldsets()


class LoginSettingsAdmin(SplitConstanceAdmin):
    change_list_form = LoginConstanceForm
    config_fieldsets = get_auth_fieldsets()


class ModuleSettingsAdmin(SplitConstanceAdmin):
    config_fieldsets = get_module_fieldsets()


class SiteSettingsAdmin(SplitConstanceAdmin):
    config_fieldsets = get_site_fieldsets()


try:
    admin.site.unregister([Config])
except NotRegistered:
    pass

admin.site.register([ThemeSettings], ThemeSettingsAdmin)
admin.site.register([LoginSettings], LoginSettingsAdmin)
admin.site.register([ModuleSettings], ModuleSettingsAdmin)
admin.site.register([SiteSettings], SiteSettingsAdmin)
