from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from rest_framework_simplejwt.models import TokenUser


class User(AbstractUser):
    class Permission:
        USER = 1
        SUPPORT = 8 | USER
        SUPERUSER = 64 | SUPPORT | USER

    token = models.TextField()
    is_blocked = models.BooleanField(default=False)
    permission = models.IntegerField(default=Permission.USER)

    @staticmethod
    def has_permission(user, permission):
        return bool(user.permission & permission)


class JWTTokenUser(TokenUser):
    @cached_property
    def permission(self):
        return self.token.get('permission', '')
