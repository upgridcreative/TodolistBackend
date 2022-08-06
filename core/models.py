from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.custom_manager import CustomUserManager

from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin as OutstandingTokenDefaultAdmin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(_('name'), max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    email_verified = models.BooleanField(default=False)

    def mark_verified(self):
        self.email_verified = True
        self.save()

    def __str__(self):
        return self.name or 'Not provided'


class VerifyEmailKey(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    key = models.CharField(max_length=6, null=True)
    generated_at = models.DateField(null=True)


class OutstandingTokenAdmin(OutstandingTokenDefaultAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True  # check if it is superuser

