import json

from django.contrib.auth import get_user_model

from apps.accounts.backends import AudienciasAuthBackend
from apps.accounts.middlewares import AudienciasRemoteUser


def _local_permission_state(request, remote_user=None):
    username = remote_user or request.META.get('HTTP_AUTH_USER')
    if username:
        user = get_user_model().objects.filter(username=username).first()
        if user is not None:
            return user.is_staff, user.is_superuser

    payload = request.META.get('HTTP_REMOTE_USER_DATA')
    if not payload:
        return False, False

    try:
        email = json.loads(payload).get('email')
    except (TypeError, ValueError):
        return False, False

    if not email:
        return False, False

    user = get_user_model().objects.filter(email=email).first()
    if user is None:
        return False, False
    return user.is_staff, user.is_superuser


def _restore_local_permissions(user, permission_state):
    is_staff, is_superuser = permission_state
    changed_fields = []
    if user.is_staff != is_staff:
        user.is_staff = is_staff
        changed_fields.append('is_staff')
    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        changed_fields.append('is_superuser')
    if changed_fields:
        user.save(update_fields=changed_fields)


class PermissionPreservingAudienciasAuthBackend(AudienciasAuthBackend):
    """Keep module-specific admin permissions during central SSO."""

    def authenticate(self, request, remote_user):
        permission_state = _local_permission_state(request, remote_user)
        user = super().authenticate(request, remote_user)
        if user is not None:
            _restore_local_permissions(user, permission_state)
        return user


class PermissionPreservingAudienciasRemoteUser(AudienciasRemoteUser):
    """Prevent the legacy middleware from overwriting local staff flags."""

    def process_request(self, request):
        permission_state = _local_permission_state(request)
        response = super().process_request(request)
        if request.user.is_authenticated:
            _restore_local_permissions(request.user, permission_state)
        return response
