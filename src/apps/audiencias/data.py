from django.conf import settings
from datetime import datetime
import logging
import requests


logger = logging.getLogger(__name__)


def _fetch_rooms(url, params):
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError, KeyError) as exc:
        logger.warning('Could not load audiencias rooms from %s: %s', url, exc)
        return []

    return data.get('results', [])


def get_audiencias_index_data():
    url = settings.AUDIENCIAS_UPSTREAM.rstrip('/') + '/api/room/'
    today = datetime.today().strftime('%Y-%m-%d')

    live_rooms = _fetch_rooms(url, {
        'youtube_status': 1,
        'is_visible': 'True',
        'ordering': '-date',
    })

    agenda_rooms = _fetch_rooms(url, {
        'date__gte': today,
        'youtube_status': 0,
        'is_visible': 'True',
        'ordering': 'date',
    })

    history_rooms = _fetch_rooms(url, {
        'youtube_status': 2,
        'is_visible': 'True',
        'ordering': '-date',
    })

    total_rooms = len(live_rooms) + len(agenda_rooms)
    history_limit = max(10 - total_rooms, 0)
    history_rooms = history_rooms[:history_limit]

    rooms = {}
    rooms['history_rooms'] = history_rooms
    rooms['agenda_rooms'] = agenda_rooms
    rooms['live_rooms'] = live_rooms

    return rooms
