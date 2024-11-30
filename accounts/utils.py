from django.core.cache import cache

from rest_framework.permissions import BasePermission


# to check if the user auth token is not in blacklist
class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        cache_token = cache.get('token_blacklist')
        if cache_token and str(token) in cache_token:
            return False
        return True
