import requests
import json

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import (Gateway, Payment)
from subscriptions.models import (Subscription, Package)
from .serializers import GatewaySerializer


class GatewayView(APIView):
    def get(self, request):
        query = Gateway.objects.filter(is_enabled=True)
        serializer = GatewaySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendRequestGatewayView(APIView):
    permission_classes = [IsAuthenticated]

    sandbox = 'sandbox'
    if settings.SANDBOX:
        sandbox = 'www'
    ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

    currency = 'IRT'
    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
    call_back_url = '/payments/verify-request-gateway/'

    def post(self, request):
        amount = request.data.get('amount')
        phone = request.user.phone_number

        data = {
            'MerchantID': settings.MERCHANT,
            'Amount': amount,
            'Description': self.description,
            'CallbackURL': self.call_back_url,
            'currency': self.currency,
            'Phone': phone
        }
        data = json.dumps(data)
        headers = {
            'content-type': 'application/json', 'content-length': str(len(data))
        }

        try:
            response = requests.post(self.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    request.session['Authority'] = str(response['Authority'])
                    request.session['PackageId'] = request.data.get('package_id')
                    request.session['Amount'] = amount
                    return Response({
                        'status': True,
                        'url': self.ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']
                    })
                else:
                    return Response({
                        'status': False,
                        'code': str(response['Status'])
                    })
            return Response({
                'status': 'status_code was not 200',
                'response': response
            })
        except requests.exceptions.Timeout:
            return Response({
                'status': False,
                'code': 'timeout'
            })
        except requests.exceptions.ConnectionError:
            return Response({
                'status': False,
                'code': 'connection error'
            })


class VerifyRequestGatewayView(APIView):
    permission_classes = [IsAuthenticated]

    sandbox = 'sandbox'
    if settings.SANDBOX:
        sandbox = 'www'
    ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"

    def post(self, request):
        amount = request.session.get('Amount')
        authority = request.session.get('Authority')
        package = get_object_or_404(Package, pk=request.session.get('PackageId'))

        data = {
            'MerchantID': settings.MERCHANT,
            'Amount': amount,
            'Authority': authority,
        }
        data = json.dumps(data)

        headers = {
            'content-type': 'application/json', 'content-length': str(len(data))
        }

        response = requests.post(self.ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                Payment.objects.create(
                    user=request.user,
                    package=package,
                    gateway='ZarinPal',
                    amount=amount,
                    status=10,
                    phone_number=request.user.phone_number,
                    consumed_code=response['RefID']
                )
                Subscription.objects.create(
                    user=request.user,
                    package=package,
                    expires_at=timezone.now() + timezone.timedelta(package.duration.days)

                )
                return Response({
                    'status': True,
                    'RefID': response['RefID']
                })
            else:
                return Response({
                    'status': response['Status'],
                    'RefID': response['RefID'],
                    'PhonNumber': request.user.phone_number,
                    'Amount': amount
                })
        return Response({
            'status': 'status_code was not 200',
            'response': response,
            'PhonNumber': request.user.phone_number,
            'Amount': amount
        })
