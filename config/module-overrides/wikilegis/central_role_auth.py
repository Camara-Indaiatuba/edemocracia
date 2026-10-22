import json

from accounts.backends import WikilegisAuthBackend
from accounts.middlewares import WikilegisRemoteUser
from wikilegis.central_roles import sync_central_roles


def _remote_user_data(request):
    payload = request.META.get('HTTP_REMOTE_USER_DATA')
    if not payload:
        return {}
    try:
        return json.loads(payload)
    except (TypeError, ValueError):
        return {}


class CentralRoleWikilegisAuthBackend(WikilegisAuthBackend):
    def authenticate(self, request, remote_user):
        user = super().authenticate(request, remote_user)
        if user is not None:
            remote_data = _remote_user_data(request)
            if 'groups' in remote_data:
                sync_central_roles(user, remote_data)
        return user


class CentralRoleWikilegisRemoteUser(WikilegisRemoteUser):
    def process_request(self, request):
        response = super().process_request(request)
        if request.user.is_authenticated:
            remote_data = _remote_user_data(request)
            if 'groups' in remote_data:
                sync_central_roles(request.user, remote_data)
        return response
