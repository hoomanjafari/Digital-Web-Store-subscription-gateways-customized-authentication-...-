from django.contrib import admin

from .models import (Gateway, Payment)


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enabled']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'gateway', 'status', 'consumed_code']
    search_fields = ['user', 'consumed_code', 'phone_number']
