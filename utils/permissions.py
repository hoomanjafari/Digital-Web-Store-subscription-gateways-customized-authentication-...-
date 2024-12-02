from django.core.cache import cache
from django.utils import timezone

from rest_framework.permissions import BasePermission

from subscriptions.models import Subscription


# to check if the user auth token is not in blacklist
class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        cache_token = cache.get('token_blacklist')
        if cache_token and str(token) in cache_token:
            return False
        return True


# to check if user has active subscription
class IsSubscriptionActive(BasePermission):
    def has_permission(self, request, view):
        query = Subscription.objects.filter(
            user=request.user,
            expires_at__gt=timezone.now()
        ).exists()
        if not query:
            return False
        return True
