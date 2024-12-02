from django.urls import path
from . import views


urlpatterns = [
    path('gateways/', views.GatewayView.as_view(), name='gateways'),

    # gateway requests
    path('send-request-gateway/', views.SendRequestGatewayView.as_view(), name='send-request-gateway'),
    path('verify-request-gateway/', views.VerifyRequestGatewayView.as_view(), name='verify-request-gateway'),
]
