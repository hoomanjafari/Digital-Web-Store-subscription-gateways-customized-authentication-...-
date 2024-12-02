from django.contrib import admin

from .models import (Package, Subscription)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration', 'is_enabled')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package')
    search_fields = ('user',)
