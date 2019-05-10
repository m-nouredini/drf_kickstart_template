from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from user.models import User


def authorize(permission=User.Permission.USER):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.user and not isinstance(request.user, AnonymousUser):
                if User.has_permission(request.user, permission):
                    return func(*args, **kwargs)
                else:
                    raise PermissionDenied(detail="User does not have sufficient permission")
            else:
                raise NotAuthenticated(detail="Authentication required")

        return wrapper

    return decorator_func
