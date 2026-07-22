EXTERNAL_IDENTITY_PROVIDERS = {
    'govbr': 'Gov.br',
    'google-oauth2': 'Google',
}


def get_external_identity_providers(user):
    if not getattr(user, 'is_authenticated', False):
        return []

    try:
        providers = user.social_auth.values_list('provider', flat=True)
    except Exception:
        return []

    return [
        EXTERNAL_IDENTITY_PROVIDERS[provider]
        for provider in providers
        if provider in EXTERNAL_IDENTITY_PROVIDERS
    ]


def user_uses_external_identity(user):
    return bool(get_external_identity_providers(user))
