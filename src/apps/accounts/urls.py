from django.urls import path, include, re_path
from apps.accounts.views import (
    CustomRegistrationView,
    ProfileView,
    ajax_csrf,
    ajax_login,
    ajax_sync_sessions,
    global_logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from apps.accounts.forms import CustomPasswordResetForm


urlpatterns = [
    path('', include('registration.backends.default.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('ajax/signup/', CustomRegistrationView.as_view(),
         name='registration_register'),
    path('ajax/login/', ajax_login, name="ajax_login"),
    path('ajax/csrf/', ajax_csrf, name="ajax_csrf"),
    path('ajax/sync-sessions/', ajax_sync_sessions,
         name="ajax_sync_sessions"),
    path('global-logout/', global_logout, name="global_logout"),
]

urlpatterns += [
    re_path(r'^logout/$',
            auth_views.LogoutView.as_view(
                next_page='/',
                template_name='registration/logout.html'),
            name='auth_logout'),
    re_path(r'^password/change/$',
            auth_views.PasswordChangeView.as_view(
                success_url=reverse_lazy('auth_password_change_done')),
            name='auth_password_change'),
    re_path(r'^password/change/done/$',
            auth_views.PasswordChangeDoneView.as_view(),
            name='auth_password_change_done'),
    re_path(r'^password/reset/$',
            auth_views.PasswordResetView.as_view(
                form_class=CustomPasswordResetForm,
                success_url=reverse_lazy('auth_password_reset_done')),
            name='auth_password_reset'),
    re_path(r'^password/reset/complete/$',
            auth_views.PasswordResetCompleteView.as_view(),
            name='auth_password_reset_complete'),
    re_path(r'^password/reset/done/$',
            auth_views.PasswordResetDoneView.as_view(),
            name='auth_password_reset_done'),
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            auth_views.PasswordResetConfirmView.as_view(
                success_url=reverse_lazy('auth_password_reset_complete')),
            name='auth_password_reset_confirm'),
]
