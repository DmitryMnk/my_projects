from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    second_name = models.CharField(max_length=20, verbose_name='Отчество', blank=True, null=True)
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    code = models.IntegerField(verbose_name='Код активации', blank=True, null=True)
    email_confirmed = models.BooleanField(default=False, verbose_name='e-mail подтверждён')
    phone_confirmed = models.BooleanField(default=False, verbose_name='номер телефона подтверждён')


class PreRegistrationData(models.Model):
    email = models.EmailField(verbose_name='e-mail', unique=True)
    code = models.IntegerField(verbose_name='Код активации', blank=True, null=True)
    time_sending = models.DateTimeField(verbose_name='Время отправления', blank=True, null=True)