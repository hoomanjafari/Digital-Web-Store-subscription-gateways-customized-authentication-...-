from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import (Subscription, Package)
from .serializers import (PackageSerializer, SubscriptionSerializer)


class PackageView(APIView):
    def get(self, request):
        query = Package.objects.filter(is_enabled=True)
        serializer = PackageSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Subscription.objects.filter(user=request.user, expires_at__gt=timezone.now())
        serializer = SubscriptionSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
