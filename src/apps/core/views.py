from django.conf import settings
from revproxy.views import DiazoProxyView
from django.shortcuts import render
import json

from apps.discourse.data import get_discourse_index_data
from apps.wikilegis.data import get_wikilegis_index_data
from apps.pautas.data import get_pautas_index_data
from apps.audiencias.data import get_audiencias_index_data


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
