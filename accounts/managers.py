import random
from django.contrib.auth.models import BaseUserManager

from . import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number required !')

        # to create a username if Username is None
        if extra_fields.get('is_superuser') is True:
            if username is None:
                username = random.choice('abcdefghijkllmnopqrstuvwxyz') + str(phone_number)[4:]
            while models.User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        user = self.model(
            phone_number=phone_number,
            username=username,
            **extra_fields,
        )
        if password:
            user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('for superuser is_staff required !')
        elif extra_fields.get('is_superuser') is not True:
            raise ValueError('for superuser is_superuser required !')
        elif extra_fields.get('is_active') is not True:
            raise ValueError('for superuser is_active required !')

        return self.create_user(phone_number, username, password, **extra_fields)
