from django.template.loader import render_to_string
from django.test import SimpleTestCase


class AudienciasCardTests(SimpleTestCase):
    def room(self, released):
        return {
            'id': 40,
            'is_access_released': released,
            'reunion_theme': 'Audiência agendada',
            'reunion_type': 'Audiência Pública',
            'legislative_body_initials': 'CFO',
            'questions_count': 0,
            'date': '2026-11-11T18:00:00-03:00',
        }

    def test_future_audience_card_is_not_a_link(self):
        html = render_to_string('audiencias-card.html', {
            'status': 'calendar',
            'room': self.room(released=False),
        })

        self.assertIn('aria-disabled="true"', html)
        self.assertNotIn('href="/audiencias/sala/40"', html)

    def test_released_audience_card_links_to_room(self):
        html = render_to_string('audiencias-card.html', {
            'status': 'calendar',
            'room': self.room(released=True),
        })

        self.assertIn('href="/audiencias/sala/40"', html)
