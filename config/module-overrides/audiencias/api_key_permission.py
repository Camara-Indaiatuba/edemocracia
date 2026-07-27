from django.conf import settings
from rest_framework import permissions


class ApiKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.GET.get('api_key') == settings.API_KEY
