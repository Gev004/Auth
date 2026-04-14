from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TokenBlacklist
from .serializers import UserSerializer, UpdateUserSerializer
from .decorators import login_required


class MeView(APIView):
    @login_required
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @login_required
    def patch(self, request):
        serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    @login_required
    def delete(self, request):
        """Soft delete: set is_active=False and blacklist the current token."""
        user = request.user
        user.is_active = False
        user.save(update_fields=["is_active"])

        token = getattr(request, "token", None)
        if token:
            TokenBlacklist.objects.get_or_create(token=token)

        return Response({"detail": "Account deactivated."}, status=status.HTTP_200_OK)
