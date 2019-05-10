from django.db import IntegrityError
from rest_framework.decorators import api_view

from service.shortcuts.exceptions import Conflict
from user.decorators import authorize
from service.shortcuts.responses import ok, created
from user.models import User
from user.serializers import UserSerializer, ServiceTokenObtainPairSerializer
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class ServiceTokenObtainPairView(TokenObtainPairView):
    serializer_class = ServiceTokenObtainPairSerializer


token_obtain_view = ServiceTokenObtainPairView().as_view()


@api_view(['POST'])
def register(request):
    user = User(username=request.data.get('username'))
    user.set_password(request.data.get('password'))
    try:
        user.save()
        return created(UserSerializer(user).data)
    except IntegrityError:
        raise Conflict()


@api_view(['GET'])
@authorize(User.Permission.USER)
def greet(request):
    return ok(f'hello {request.user.username}')


@api_view(['DELETE'])
@authorize(User.Permission.SUPPORT)
def block_user(request):
    try:
        user = User.objects.get(username=request.data.get('username'))
        user.is_blocked = True
        user.save()
        RefreshToken(user.token).blacklist()
        return ok()
    except User.DoesNotExist:
        raise NotFound(detail='User not found')
