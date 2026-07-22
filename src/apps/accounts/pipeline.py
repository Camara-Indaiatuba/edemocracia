from datetime import datetime
from requests import request, RequestException
from django.core.files.base import ContentFile
from social_core.pipeline.social_auth import associate_by_email


def associate_by_verified_email(backend, details, user=None, response=None,
                                *args, **kwargs):
    if backend.name == 'govbr':
        email_verified = bool(
            response and response.get('email_verified') is True
        )
        if not email_verified:
            id_token = getattr(backend, 'id_token', None) or {}
            email_verified = id_token.get('email_verified') is True

        if not email_verified:
            return None

    return associate_by_email(
        backend, details, user=user, response=response, *args, **kwargs
    )


def save_avatar(user, url, suffix):
    if not url or user.profile.avatar:
        user.profile.save()
        return

    try:
        response_image = request('GET', url, timeout=10)
        response_image.raise_for_status()
    except RequestException:
        user.profile.save()
    else:
        user.profile.avatar.save('{0}_{1}.jpg'.format(user.username, suffix),
                                 ContentFile(response_image.content))


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        if 'email' in response.get('denied_scopes', '') and not user.email:
            user.email = response.get('id') + '@facebook.com'
            user.save()
        user.profile.gender = response.get('gender', '')
        birthdate = response.get('birthday', '')
        if birthdate:
            user.profile.birthdate = datetime.strptime(birthdate, '%m/%d/%Y')
        location = response.get('location', '')
        if location:
            user.profile.country = location['name'].split(', ')[1]
        url = "https://graph.facebook.com/%s/picture?type=large" % response['id']
        save_avatar(user, url, 'fb')

    if backend.name == 'google-oauth2':
        user.profile.gender = response.get('gender', '')
        image = response.get('image') or {}
        url = image.get('url') or response.get('picture')

        if image.get('isDefault') or not url:
            user.profile.save()
        else:
            url = url.replace('?sz=50', '?sz=200')
            save_avatar(user, url, 'g')

    if backend.name == 'govbr':
        user.profile.save()
