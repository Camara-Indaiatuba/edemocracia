import logging

from django.contrib.auth.models import Group, Permission
from django.db.models import Q


logger = logging.getLogger(__name__)

COMMUNICATION_GROUP = 'Comunica\u00e7\u00e3o'

CENTRAL_ROLES = {
    COMMUNICATION_GROUP: (
        'core.add_bill',
        'core.change_bill',
        'core.view_bill',
        'core.add_billsegment',
        'core.change_billsegment',
        'core.delete_billsegment',
        'core.view_billsegment',
        'core.add_billreference',
        'core.change_billreference',
        'core.delete_billreference',
        'core.view_billreference',
        'core.add_billvideo',
        'core.change_billvideo',
        'core.delete_billvideo',
        'core.view_billvideo',
        'core.add_billtheme',
        'core.change_billtheme',
        'core.view_billtheme',
        'core.view_segmenttype',
        'core.change_additiveamendment',
        'core.delete_additiveamendment',
        'core.view_additiveamendment',
        'core.change_modifieramendment',
        'core.delete_modifieramendment',
        'core.view_modifieramendment',
        'core.change_supressamendment',
        'core.delete_supressamendment',
        'core.view_supressamendment',
        'core.delete_comment',
        'core.view_comment',
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
