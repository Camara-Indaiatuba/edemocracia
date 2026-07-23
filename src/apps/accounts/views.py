from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from apps.accounts.models import UserProfile
from apps.accounts.utils import (
    get_external_identity_providers,
    user_uses_external_identity,
)
from apps.audiencias.apps import AudienciasConfig
from registration.views import RegistrationView as BaseRegistrationView
from registration.models import RegistrationProfile
from registration.users import UserModel
from registration import signals
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.core.tasks import default_login
from apps.discourse.tasks import discourse_login
from apps.wikilegis.apps import WikilegisConfig
from apps.accounts import captcha
from django.views.generic import UpdateView
from django.contrib import messages
from apps.accounts.forms import UserProfileForm
from django.urls import reverse, reverse_lazy
from apps.core.auth_config import is_email_login_enabled, is_recaptcha_enabled
from apps.core.module_config import (
    is_audiencias_enabled,
    is_discourse_enabled,
    is_wikilegis_enabled,
)
import requests


GLOBAL_SESSION_COOKIES = (
    settings.SESSION_COOKIE_NAME,
    'audiencias_session',
    'wikilegis_session',
    '_forum_session',
    '_t',
)


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class CustomRegistrationView(BaseRegistrationView):
    http_method_names = ['post']
    success_url = 'registration_complete'
    template_name = 'registration/custom_registration_form.html'

    registration_profile = RegistrationProfile

    def form_invalid(self, form):
        data = {
            'data': form.errors,
        }
        return JsonResponse(data, status=400)

    def form_valid(self, form):
        if not is_email_login_enabled():
            return JsonResponse({'data': _('Cadastro por e-mail desabilitado.')},
                                status=403)

        if is_recaptcha_enabled():
            captcha_token = form.data.get('g-recaptcha-response')
            if not captcha_token:
                return JsonResponse(
                    {'data': captcha.ERRORS['missing-input-response']},
                    status=401)

            captcha_response = captcha.verify(
                captcha_token, remote_ip=get_client_ip(self.request))
            if not captcha_response.get('success'):
                message = ' '.join(
                    map(lambda x: captcha.ERRORS.get(x, x),
                        captcha_response.get('error-codes', ['bad-request']))
                )
                data = {
                    'data': message,
                }
                return JsonResponse(data, status=401)

        super().form_valid(form)
        if settings.REGISTRATION_AUTO_ACTIVATE:
            message = _("Cadastro realizado. Você já pode entrar.")
        else:
            message = _("Please check your email to complete the"
                        " registration process.")
        data = {'data': message}
        return JsonResponse(data, status=200)

    def register(self, form):
        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (UserModel().objects
                                 .create_user(**form.cleaned_data))

        profile = UserProfile.objects.get(user=new_user_instance)
        profile.uf = form.cleaned_data['uf']
        profile.country = form.cleaned_data['country']
        profile.birthdate = form.cleaned_data['birthdate']
        profile.gender = form.cleaned_data['gender']
        profile.save()

        send_activation_email = (
            not settings.REGISTRATION_AUTO_ACTIVATE
            and settings.REGISTRATION_SEND_ACTIVATION_EMAIL)

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=send_activation_email,
            request=self.request,
        )

        if settings.REGISTRATION_AUTO_ACTIVATE:
            new_user.is_active = True
            new_user.save(update_fields=['is_active'])
        elif settings.REGISTRATION_USE_RDSTATION:
            activation_key = RegistrationProfile.objects.get(
                user=new_user).activation_key

            payload = {'token_rdstation': 'd04f2153c158f0f2b17fbf43dac9489f',
                       'identificador': 'Cadastro no Wikilegis',
                       'email': new_user.email,
                       'WIKILEGIS_token': activation_key,
                       'nome': new_user.first_name}

            requests.post("https://www.rdstation.com.br/api/1.3/conversions",
                          data=payload, timeout=10)  # to send email

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def registration_allowed(self):
        return (
            is_email_login_enabled() and
            getattr(settings, 'REGISTRATION_OPEN', True)
        )


def ajax_login(request):
    if not is_email_login_enabled():
        return JsonResponse({'data': _('Login por e-mail desabilitado.')},
                            status=403)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        response_data = {}
        if form.is_valid():
            login(request, form.get_user())
            status_code = 200
        else:
            response_data['data'] = _("Invalid user and/or password.")
            status_code = 401
        return JsonResponse(response_data, status=status_code)
    else:
        return HttpResponse(status=405)


@ensure_csrf_cookie
def ajax_csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


def ajax_sync_sessions(request):
    if not request.user.is_authenticated:
        return JsonResponse({'synced': []}, status=401)

    synced = []
    if is_audiencias_enabled():
        current_cookie = request.COOKIES.get(AudienciasConfig.cookie_name)
        synced_cookie = default_login(
            request.user, request, AudienciasConfig)
        if synced_cookie and synced_cookie != current_cookie:
            synced.append('audiencias')

    if is_wikilegis_enabled():
        current_cookie = request.COOKIES.get(WikilegisConfig.cookie_name)
        synced_cookie = default_login(
            request.user, request, WikilegisConfig)
        if synced_cookie and synced_cookie != current_cookie:
            synced.append('wikilegis')

    if is_discourse_enabled() and '_t' not in request.COOKIES:
        discourse_login(sender=None, user=request.user, request=request)
        if '_t' in request.set_cookies:
            synced.append('discourse')

    return JsonResponse({'synced': synced})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def global_logout(request, next_url=None):
    next_url = (
        request.GET.get('next') or
        request.POST.get('next') or
        next_url or
        '/'
    )

    logout(request)
    response = redirect(next_url)

    for cookie_name in GLOBAL_SESSION_COOKIES:
        response.delete_cookie(cookie_name)

    return response


class ProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Perfil modificado com sucesso!')
        return reverse('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        providers = get_external_identity_providers(self.request.user)
        context.update({
            'external_identity_providers': providers,
            'uses_external_identity': bool(providers),
            'can_change_password': (
                self.request.user.has_usable_password() and not providers
            ),
        })
        return context


class LocalPasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('auth_password_change_done')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        if user_uses_external_identity(request.user):
            messages.info(
                request,
                'Esta conta usa login externo. Altere a senha no provedor de identidade.',
            )
            return redirect('profile')

        if not request.user.has_usable_password():
            messages.info(
                request,
                'Esta conta nao possui senha local no e-Democracia.',
            )
            return redirect('profile')

        return super().dispatch(request, *args, **kwargs)
