from .jwt_utils import decode_token
from .models import User, TokenBlacklist


class JWTAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            # Check blacklist
            if not TokenBlacklist.objects.filter(token=token).exists():
                payload = decode_token(token)
                if payload:
                    try:
                        user = User.objects.select_related("role").get(
                            id=payload["user_id"], is_active=True
                        )
                        request.user = user
                        request.token = token
                    except User.DoesNotExist:
                        pass
        return self.get_response(request)
