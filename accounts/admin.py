from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phone_number', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Important dates', {'fields': ('date_joined', 'last_login', 'last_seen')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'user_permissions')}),
        ('groups', {'fields': ('groups',)})

    )
    list_display = ['phone_number', 'username', 'is_staff', 'is_active']


admin.site.register(User, MyUserAdmin)
