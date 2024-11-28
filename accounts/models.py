from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        max_length=66, verbose_name='username', unique=True,
        validators=[RegexValidator(
            r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
            'Enter a valid username starting with a-z'
            'this value may contain only letters, numbers and underscore characters',
        )],
        error_messages={
            'unique': 'A user with that username already exists'
        },
        help_text='Required. 66 characters or fewer. Letters, digits and underscore',
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name='Phone Number',
        validators=[RegexValidator(
            r'^(98|0)?9\d{9}$',
            'Enter a valid phone number'
        )],
        error_messages={'unique': 'A user with that phone number already exists'},
    )

    last_seen = models.DateTimeField(verbose_name='Last Seen', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.phone_number}'
