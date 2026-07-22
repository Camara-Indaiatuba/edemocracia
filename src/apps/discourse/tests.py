from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.discourse.tasks import discourse_login


class DiscourseLoginTests(SimpleTestCase):
    @patch('apps.discourse.tasks.requests.Session')
    @patch('apps.discourse.tasks.is_discourse_enabled', return_value=False)
    def test_disabled_module_does_not_contact_discourse(
            self, _is_enabled, session):
        discourse_login(
            sender=None,
            user=SimpleNamespace(email='user@example.org'),
            request=SimpleNamespace(),
        )

        session.assert_not_called()
