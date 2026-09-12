
from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import ClassVar
from django import forms


class UserSingUp(models.Model):
    class UserStatus(models.TextChoices):
        USER_COMUM = "user_comum", ("usuario comum, ainda sem pagar")
        BETA_TEST = "beta_test", ("usuario de testes")
        USER_VIP = "user_vip", ("usuario vip")

    name = models.CharField(max_length=200, unique=False, null=True, blank=True)
    email = models.EmailField(("email address"), unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_picture", blank=True, null=True
    )
    stripe_customer_id = models.CharField(
        max_length=100, blank=True, null=True, unique=True
    )
    user_status = models.CharField(
        max_length=20, choices=UserStatus, default=UserStatus.USER_COMUM
    )

    def __str__(self):
        return str(self.username)

    @property
    def is_vip(self):
        return self.user_status == self.UserStatus.USER_VIP

    @property
    def not_vip(self):
        return self.user_status == self.UserStatus.USER_COMUM

    @property
    def is_beta(self):
        return self.user_status == self.UserStatus.BETA_TEST


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = UserSingUp
        fields = ["name", "email", "profile_picture"]
