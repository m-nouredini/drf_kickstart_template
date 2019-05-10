from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from user.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ServiceTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if not user.is_blocked:
            token = super().get_token(user)
            token['username'] = user.username
            token['permission'] = user.permission
            user.token = token
            user.save()
            return token
        else:
            raise PermissionDenied(detail="User is blocked")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
