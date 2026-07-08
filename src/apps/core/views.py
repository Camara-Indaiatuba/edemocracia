from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from revproxy.views import DiazoProxyView
import json

from apps.discourse.data import get_discourse_index_data
from apps.wikilegis.data import get_wikilegis_index_data
from apps.pautas.data import get_pautas_index_data
from apps.audiencias.data import get_audiencias_index_data
from apps.core.themes import THEME_PRESETS, get_active_theme, reset_config_colors


class EdemProxyView(DiazoProxyView):
    html5 = True

    def get_request_headers(self):
        request_headers = super().get_request_headers()
        public_host = self.request.META.get('HTTP_X_FORWARDED_HOST') or self.request.get_host()
        public_proto = self.request.META.get(
            'HTTP_X_FORWARDED_PROTO',
            'https' if self.request.is_secure() else 'http'
        )

        request_headers['Host'] = public_host
        request_headers['X-Forwarded-Host'] = public_host
        request_headers['X-Forwarded-Proto'] = public_proto

        return request_headers

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if request.user.is_authenticated:
            user_data = {
                'name': request.user.first_name,
                'email': request.user.email,
            }

            request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)

        return super(EdemProxyView, self).dispatch(request, *args, **kwargs)


def index(request):
    context = {}
    if settings.PAUTAS_ENABLED:
        context['pautas'] = get_pautas_index_data()

    if settings.WIKILEGIS_ENABLED:
        context['bills'] = get_wikilegis_index_data()

    if settings.DISCOURSE_ENABLED:
        context['topics'] = get_discourse_index_data()

    if settings.AUDIENCIAS_ENABLED:
        rooms = get_audiencias_index_data()

        context['history_rooms'] = rooms['history_rooms']
        context['agenda_rooms'] = rooms['agenda_rooms']
        context['live_rooms'] = rooms['live_rooms']

    return render(request, 'index.html', context)


def theme_css(request):
    css = render_to_string(
        'components/theme-overrides.css',
        {'active_theme': get_active_theme()},
        request=request,
    )
    response = HttpResponse(css, content_type='text/css')
    response['Cache-Control'] = 'no-store'
    return response


@staff_member_required
def reset_theme_colors(request):
    from constance import config

    selected_theme = request.GET.get('theme')
    if selected_theme not in THEME_PRESETS:
        messages.error(request, 'Selecione um tema editavel para restaurar as cores.')
    elif reset_config_colors(config, selected_theme):
        messages.success(request, 'Cores padrao do tema restauradas.')

    return redirect('/admin/core/theme_settings/')
