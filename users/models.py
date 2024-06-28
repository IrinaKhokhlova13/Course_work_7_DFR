from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    telegram_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='id в телеграм')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
