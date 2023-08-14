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
    first_name = models.CharField(_('first_name'), max_length=30)
    last_name = models.CharField(_('last_name'), max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = CustomUserManager()

    email_verified = models.BooleanField(default=False)

    def mark_verified(self):
        self.email_verified = True
        self.save()

    def __str__(self):
        return self.first_name or 'Not provided'

    def is_verified(self):
        return self.email_verified

    def get_updatible_fields(self):
        return [
            'first_name',
            'last_name',
        ]


class VerifyEmailKey(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    key = models.CharField(max_length=6, null=True)
    generated_at = models.DateField(null=True)


class OutstandingTokenAdmin(OutstandingTokenDefaultAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True  # check if it is superuser


class Categories(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    temp_id = models.CharField(max_length=100)
    on_server_creation_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30, null=False)
    color = models.CharField(max_length=10, null=True,default='Remove later')
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        self.on_server_creation_time = timezone.now()
        return super().save(*args, **kwargs)

    def get_updatible_fields(self):
        return [
            'title',
            'color'
        ]

    def delete_catagory(self):
        self.is_deleted = True
        self.save()


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)  # Owner of the task
    temp_id = models.CharField(max_length=100, unique=True, null=True)
    parent_temp_id = models.CharField(max_length=70, null=True)
    parent = models.ForeignKey('Task', null=True, on_delete=models.CASCADE)
    child_order = models.IntegerField(default=-1)
    on_server_creation_time = models.DateTimeField(auto_now=True)
    catagory = models.ForeignKey(
        Categories, null=True, on_delete=models.SET_NULL)
    content = models.CharField(max_length=200)
    discription = models.TextField(max_length=5000, null=True)
    due = models.DateField(null=True)
    priorty = models.IntegerField(default=4)
    is_checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        self.on_server_creation_time = timezone.now()
        return super().save(*args, **kwargs)

    def setParent(self, parent, child_order):
        self.parent = parent
        self.parent_temp_id = parent.temp_id
        self.child_order = child_order

    def get_required_fields(self):
        return [
            'user',
            'temp_id',
            'content',
        ]

    def delete_task(self):
        self.is_deleted = True
        self.save()
