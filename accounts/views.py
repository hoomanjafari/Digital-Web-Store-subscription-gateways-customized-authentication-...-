import random

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import (RefreshToken, AccessToken, BlacklistedToken)

from .models import User
from .serializers import UserSerializer


class UserRegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp_cache = cache.get(str(phone_number))            # cache.set('keyName', 'value', 'expireTime')
        if not otp_cache:                                   # cache.get('keyName')
            otp = random.randint(1000, 9999)
            cache.set(str(phone_number), otp, 30)
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    phone_number=phone_number,
                    is_active=False,
                )
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'otp': 'not_expired'}, status=status.HTTP_403_FORBIDDEN)


class UserLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        otp_cache = cache.get(phone_number)
        print(otp_cache)
        if not otp_cache:
            return Response({'detail': 'otp_is_expired'}, status=status.HTTP_403_FORBIDDEN)
        if str(otp_cache) != str(otp):
            return Response({'detail': 'incorrect_otp'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(phone_number=str(phone_number))
            if user.is_active is False:
                user.is_active = True
                user.save()
            # authentication
            access_token = AccessToken.for_user(user=user)
            refresh_token = RefreshToken.for_user(user=user)
            return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'user_not_found'}, status=status.HTTP_403_FORBIDDEN)


class UserLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'user_logged_out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
