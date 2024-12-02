from django.db import models

from utils.validators import validate_phone_number


class Gateway(models.Model):
    title = models.CharField(max_length=66, verbose_name='Title')
    description = models.TextField(verbose_name='Descriptions')
    avatar = models.ImageField(upload_to='gateways/img/%y%m%d%H%M', null=True, blank=True, verbose_name='Avatar')
    is_enabled = models.BooleanField(default=True, verbose_name='Enabled')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'

    def __str__(self):
        return f'{self.title}'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCELED = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = (
        (STATUS_VOID, 'Void'),
        (STATUS_PAID, 'Paid'),
        (STATUS_ERROR, 'Error'),
        (STATUS_CANCELED, 'User Canceled'),
        (STATUS_REFUNDED, 'Refunded')
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payments')
    package = models.ForeignKey('subscriptions.Package', on_delete=models.CASCADE, related_name='payments')
    gateway = models.ForeignKey('Gateway', on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveIntegerField(verbose_name='Price paid')
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=STATUS_VOID, verbose_name='Status')
    device_uuid = models.CharField(max_length=66, null=True, blank=True, verbose_name='Device UUID')
    phone_number = models.CharField(max_length=11, validators=[validate_phone_number], verbose_name='Phone number')
    consumed_code = models.PositiveIntegerField(verbose_name='Consumed reference code') # code peygiri
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.user} - {self.phone_number}'
