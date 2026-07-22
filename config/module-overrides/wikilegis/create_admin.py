import os

import django


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'wikilegis.settings.wikilegis',
)


def create_superuser():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    admin_email = os.environ.get('ADMIN_EMAIL', '').strip()
    admin_password = os.environ.get('ADMIN_PASSWORD', '')

    if not admin_email or not admin_password:
        print(
            'Skipping superuser creation: missing ADMIN_EMAIL or '
            'ADMIN_PASSWORD environment variable.'
        )
        return

    user, created = User.objects.get_or_create(email=admin_email)
    if created:
        user.set_password(admin_password)

    user.is_active = True
    user.is_superuser = True
    user.is_staff = True
    user.save()

    if created:
        print('Initial Wikilegis administrator created.')
    else:
        print(
            'Initial Wikilegis administrator already exists; '
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
    print('Wikilegis site information updated.')


if __name__ == '__main__':
    django.setup()
    create_superuser()
    update_sites()
