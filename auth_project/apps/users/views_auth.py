from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, TokenBlacklist
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .password_utils import hash_password, verify_password
from .jwt_utils import create_token
from .decorators import login_required
from apps.access.models import Role


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Assign default "user" role
        try:
            default_role = Role.objects.get(name="user")
        except Role.DoesNotExist:
            default_role = None

        user = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data.get("middle_name", ""),
            email=data["email"],
            password_hash=hash_password(data["password"]),
            role=default_role,
        )

        token = create_token(user.id)
        return Response(
            {"token": token, "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = User.objects.select_related("role").get(email=data["email"])
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "This account has been deactivated."}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not verify_password(data["password"], user.password_hash):
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )

        token = create_token(user.id)
        return Response({"token": token, "user": UserSerializer(user).data})


class LogoutView(APIView):
    @login_required
    def post(self, request):
        token = getattr(request, "token", None)
        if token:
            TokenBlacklist.objects.get_or_create(token=token)
        return Response({"detail": "Successfully logged out."})
