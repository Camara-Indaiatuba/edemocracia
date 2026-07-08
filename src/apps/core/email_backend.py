from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

from apps.core.auth_config import get_smtp_config


class ConfigurableEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.kwargs = kwargs

    def _backend(self):
        smtp = get_smtp_config()
        if not smtp['host']:
            return ConsoleEmailBackend(fail_silently=self.fail_silently)

        return SMTPEmailBackend(
            host=smtp['host'],
            port=smtp['port'],
            username=smtp['username'],
            password=smtp['password'],
            use_tls=smtp['use_tls'],
            use_ssl=smtp['use_ssl'],
            fail_silently=self.fail_silently,
            **self.kwargs,
        )

    def send_messages(self, email_messages):
        smtp = get_smtp_config()
        default_from_email = smtp['default_from_email']
        if default_from_email:
            for message in email_messages:
                if (not message.from_email or
                        message.from_email == settings.DEFAULT_FROM_EMAIL):
                    message.from_email = default_from_email

        return self._backend().send_messages(email_messages)
