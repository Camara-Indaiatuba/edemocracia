import logging

from django.contrib.auth.models import Group, Permission
from django.db.models import Q


logger = logging.getLogger(__name__)

COMMUNICATION_GROUP = 'Comunica\u00e7\u00e3o'
LEGACY_GROUP_NAMES = ('Comunicacao',)

CENTRAL_ROLES = {
    COMMUNICATION_GROUP: (
        'core.add_room',
        'core.change_room',
        'core.view_room',
        'core.add_roomattachment',
        'core.change_roomattachment',
        'core.delete_roomattachment',
        'core.view_roomattachment',
        'core.add_video',
        'core.change_video',
        'core.delete_video',
        'core.view_video',
        'core.change_question',
        'core.delete_question',
        'core.view_question',
        'core.delete_message',
        'core.view_message',
    ),
}


def _permissions_for(labels):
    query = Q(pk__in=[])
    for label in labels:
        app_label, codename = label.split('.', 1)
        query |= Q(
            content_type__app_label=app_label,
            codename=codename,
        )
    return Permission.objects.filter(query)


def ensure_central_groups():
    for name, labels in CENTRAL_ROLES.items():
        group, _ = Group.objects.get_or_create(name=name)
        permissions = list(_permissions_for(labels))
        found = {
            '{}.{}'.format(
                permission.content_type.app_label,
                permission.codename,
            )
            for permission in permissions
        }
        missing = sorted(set(labels) - found)
        if missing:
            logger.warning(
                'Central role %s has unavailable permissions: %s',
                name,
                ', '.join(missing),
            )
        group.permissions.set(permissions)

        for legacy_name in LEGACY_GROUP_NAMES:
            legacy_group = Group.objects.filter(name=legacy_name).first()
            if legacy_group is None:
                continue
            group.user_set.add(*legacy_group.user_set.all())
            legacy_group.delete()


def sync_central_roles(user, remote_data):
    ensure_central_groups()
    remote_groups = set(remote_data.get('groups') or ())
    managed_names = set(CENTRAL_ROLES)

    for name in managed_names:
        group = Group.objects.get(name=name)
        if name in remote_groups:
            user.groups.add(group)
        else:
            user.groups.remove(group)

    has_central_role = bool(remote_groups & managed_names)
    has_local_access = (
        user.groups.exclude(name__in=managed_names).exists()
        or user.user_permissions.exists()
    )
    should_be_staff = bool(
        remote_data.get('is_staff')
        or remote_data.get('is_superuser')
        or has_central_role
        or has_local_access
    )
    if user.is_staff != should_be_staff:
        user.is_staff = should_be_staff
        user.save(update_fields=['is_staff'])
