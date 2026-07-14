from django.utils.translation import gettext_lazy as _
import requests

from apps.core.auth_config import get_recaptcha_keys


ERRORS = {
    'missing-input-secret': _('reCAPTCHA: The secret parameter is missing.'),
    'invalid-input-secret': _('reCAPTCHA: The secret parameter is invalid'
                              ' or malformed.'),
    'missing-input-response': _('reCAPTCHA: The response parameter'
                                ' is missing.'),
    'invalid-input-response': _('reCAPTCHA: The response parameter is invalid'
                                ' or malformed.'),
    'bad-request': _('reCAPTCHA: The request is invalid or malformed.'),
}


def verify(captcha_response, remote_ip=None):
    _, private_key = get_recaptcha_keys()
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': private_key,
        'response': captcha_response,
    }

    if remote_ip:
        params['remoteip'] = remote_ip

    try:
        verify_response = requests.post(url, data=params, timeout=10)
        verify_response.raise_for_status()
        return verify_response.json()
    except (requests.RequestException, ValueError):
        return {'success': False, 'error-codes': ['bad-request']}
