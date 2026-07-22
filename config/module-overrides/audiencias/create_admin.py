import os

import django


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'audiencias_publicas.settings',
)


def create_superuser():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    admin_email = os.environ.get('ADMIN_EMAIL', '').strip()
    admin_username = os.environ.get('ADMIN_USERNAME', '').strip()
    admin_password = os.environ.get('ADMIN_PASSWORD', '')

    if not admin_email or not admin_username or not admin_password:
        print(
            'Skipping superuser creation: missing ADMIN_EMAIL, '
            'ADMIN_USERNAME or ADMIN_PASSWORD environment variable.'
        )
        return

    user = User.objects.filter(email__iexact=admin_email).first()
    if user is None:
        user = User.objects.filter(username=admin_username).first()

    created = user is None
    if created:
        user = User(username=admin_username, email=admin_email)
        user.set_password(admin_password)
    else:
        if not user.email:
            user.email = admin_email

        username_taken = (
            User.objects
            .filter(username=admin_username)
            .exclude(pk=user.pk)
            .exists()
        )
        if not username_taken:
            user.username = admin_username

    user.is_active = True
    user.is_superuser = True
    user.is_staff = True
    user.save()

    if created:
        print('Initial Audiencias administrator created.')
    else:
        print(
            'Initial Audiencias administrator already exists; '
            'permissions were checked and password was preserved.'
        )


def update_sites():
    import re

    from django.contrib.sites.models import Site

    site_domain = os.environ.get('SITE_DOMAIN', '').strip()
    site_name = os.environ.get('SITE_NAME', '').strip()
    if not site_domain or not site_name:
        print(
            'Skipping site update: missing SITE_DOMAIN or SITE_NAME '
            'environment variable.'
        )
        return

    site = Site.objects.get_current()
    site.domain = re.sub(r'^(http|https)://', '', site_domain)
    site.name = site_name
    site.save()
    print('Audiencias site information updated.')


if __name__ == '__main__':
    django.setup()
    create_superuser()
    update_sites()
