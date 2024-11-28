from django.urls import path

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from . import views


urlpatterns = [
    path('user-register/', views.UserRegisterView.as_view(), name='user-register'),
    path('user-login/', views.UserLoginView.as_view(), name='user-login'),

    # token creating for user authentication by simplejwt
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', views.UserLogoutView.as_view(), name='user-logout'),
]
