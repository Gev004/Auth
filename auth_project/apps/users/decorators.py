from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def login_required(func):
    
    @wraps(func)
    def wrapper(self_or_request, *args, **kwargs):
        request = self_or_request if not hasattr(self_or_request, 'request') else self_or_request.request
        if hasattr(self_or_request, 'get'):
            request = args[0] if args else getattr(self_or_request, '_request', None)
            return func(self_or_request, *args, **kwargs) if _check_user(args[0] if args else None) else _401()
        return func(self_or_request, *args, **kwargs) if _check_user(request) else _401()
    return wrapper


def _check_user(request):
    return request is not None and getattr(request, 'user', None) is not None


def _401():
    return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)


def _403():
    return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)


def login_required(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        if not getattr(request, 'user', None):
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        return func(view_self, request, *args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        if not getattr(request, 'user', None):
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.role or request.user.role.name != "admin":
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        return func(view_self, request, *args, **kwargs)
    return wrapper
