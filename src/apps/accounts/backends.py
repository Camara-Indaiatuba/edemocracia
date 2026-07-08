from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from social_core.backends.google import GoogleOAuth2

from apps.core.auth_config import get_google_credentials


class ConfigurableGoogleOAuth2(GoogleOAuth2):
    def get_key_and_secret(self):
        return get_google_credentials()


class AuthenticationEmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        username = username or kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
