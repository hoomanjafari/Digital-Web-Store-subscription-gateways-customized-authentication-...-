from django.db import models

from utils.validators import validate_sku


class Package(models.Model):
    title = models.CharField(max_length=66, verbose_name='Title')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    sku = models.CharField(max_length=20, validators=[validate_sku], verbose_name='Stock Keeping Unit')
    avatar = models.ImageField(upload_to='packages/img/%y%m%d%H%M', verbose_name='Avatar', blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='Price')
    duration = models.DurationField(verbose_name='Duration', blank=True, null=True)
    is_enabled = models.BooleanField(default=True, verbose_name='Enabled')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __str__(self):
        return f'{self.title}'


class Subscription(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='subscriptions')
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Expires at')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f'{self.user} - {self.package}'

