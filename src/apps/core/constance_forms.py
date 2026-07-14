from constance.forms import ConstanceForm
from django import forms


class ThemeConstanceForm(ConstanceForm):
    pass


class LoginConstanceForm(ConstanceForm):
    secret_fields = (
        'LOGIN_GOOGLE_OAUTH2_SECRET',
        'LOGIN_EMAIL_HOST_PASSWORD',
        'LOGIN_RECAPTCHA_PRIVATE_KEY',
    )

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.secret_fields:
            if not cleaned_data.get(field_name):
                cleaned_data[field_name] = self.initial.get(field_name, '')

        email_enabled = cleaned_data.get('LOGIN_EMAIL_ENABLED')
        google_enabled = cleaned_data.get('LOGIN_GOOGLE_ENABLED')

        if not email_enabled and not google_enabled:
            raise forms.ValidationError(
                'Mantenha pelo menos uma forma de login habilitada.'
            )

        if google_enabled:
            if not cleaned_data.get('LOGIN_GOOGLE_OAUTH2_KEY'):
                self.add_error(
                    'LOGIN_GOOGLE_OAUTH2_KEY',
                    'Informe o Client ID para habilitar login com Google.',
                )
            if not cleaned_data.get('LOGIN_GOOGLE_OAUTH2_SECRET'):
                self.add_error(
                    'LOGIN_GOOGLE_OAUTH2_SECRET',
                    'Informe o Client secret para habilitar login com Google.',
                )

        if email_enabled:
            if not cleaned_data.get('LOGIN_EMAIL_HOST'):
                self.add_error(
                    'LOGIN_EMAIL_HOST',
                    'Informe o servidor SMTP para habilitar login por e-mail.',
                )
            if not cleaned_data.get('LOGIN_DEFAULT_FROM_EMAIL'):
                self.add_error(
                    'LOGIN_DEFAULT_FROM_EMAIL',
                    'Informe o remetente padrao dos e-mails.',
                )

        if (cleaned_data.get('LOGIN_EMAIL_USE_TLS') and
                cleaned_data.get('LOGIN_EMAIL_USE_SSL')):
            self.add_error(
                'LOGIN_EMAIL_USE_SSL',
                'Escolha TLS ou SSL, nao os dois ao mesmo tempo.',
            )

        if cleaned_data.get('LOGIN_RECAPTCHA_ENABLED'):
            if not cleaned_data.get('LOGIN_RECAPTCHA_SITE_KEY'):
                self.add_error(
                    'LOGIN_RECAPTCHA_SITE_KEY',
                    'Informe a chave publica para habilitar o reCAPTCHA.',
                )
            if not cleaned_data.get('LOGIN_RECAPTCHA_PRIVATE_KEY'):
                self.add_error(
                    'LOGIN_RECAPTCHA_PRIVATE_KEY',
                    'Informe a chave secreta para habilitar o reCAPTCHA.',
                )

        return cleaned_data
