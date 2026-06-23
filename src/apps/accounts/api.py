from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import filters, generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters import FilterSet
from django_filters import rest_framework as django_filters
from apps.accounts.serializers import UserSerializer


class HasInternalApiKey(permissions.BasePermission):

    def has_permission(self, request, view):
        api_key = getattr(settings, 'INTERNAL_API_KEY', '')
        return bool(api_key and request.GET.get('api_key') == api_key)


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'last_login': ['lt', 'gt', 'lte', 'gte', 'year__gt', 'year__lt'],
            'date_joined': ['lt', 'gt', 'lte', 'gte', 'year__gt', 'year__lt'],
            'profile__birthdate': ['lt', 'gt', 'lte', 'gte', 'year__gt',
                                   'year__lt'],
            'profile__uf': ['exact'],
            'profile__gender': ['exact'],
            'profile__country': ['exact'],
        }


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (HasInternalApiKey,)
    filter_class = UserFilter
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
    )
    filter_fields = ('id', 'profile__uf')
    search_fields = ('username', 'first_name', 'last_name')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user_list_api',
                         request=request, format=format),
    })
