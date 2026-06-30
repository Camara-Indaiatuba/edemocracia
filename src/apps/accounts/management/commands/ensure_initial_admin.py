import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update the initial administrative user from env vars.'

    def handle(self, *args, **options):
        email = os.environ.get('ADMIN_EMAIL', '').strip()
        username = os.environ.get('ADMIN_USERNAME', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '')

        if not email or not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Skipping initial admin creation: ADMIN_EMAIL, '
                    'ADMIN_USERNAME or ADMIN_PASSWORD is missing.'
                )
            )
            return

        User = get_user_model()
        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            user = User.objects.filter(username=username).first()

        created = user is None
        if created:
            user = User(username=username, email=email)
            user.set_password(password)
        else:
            if not user.email:
                user.email = email
            if username and user.username != username:
                username_taken = (
                    User.objects
                    .filter(username=username)
                    .exclude(pk=user.pk)
                    .exists()
                )
                if not username_taken:
                    user.username = username
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            'Initial admin username already belongs to '
                            'another user; keeping current username.'
                        )
                    )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    'Initial admin user created for %s.' % email
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Initial admin user already exists for %s; permissions '
                    'were checked and password was preserved.' % email
                )
            )
