from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Role, BusinessElement, AccessRoleRule
from .serializers import RoleSerializer, BusinessElementSerializer, AccessRoleRuleSerializer
from apps.users.decorators import login_required, admin_required


class RoleListView(APIView):
    @admin_required
    def get(self, request):
        return Response(RoleSerializer(Role.objects.all(), many=True).data)


class BusinessElementListView(APIView):
    @admin_required
    def get(self, request):
        return Response(BusinessElementSerializer(BusinessElement.objects.all(), many=True).data)


class AccessRuleListCreateView(APIView):
    @admin_required
    def get(self, request):
        rules = AccessRoleRule.objects.select_related("role", "element").all()
        return Response(AccessRoleRuleSerializer(rules, many=True).data)

    @admin_required
    def post(self, request):
        serializer = AccessRoleRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessRuleDetailView(APIView):
    def _get_rule(self, pk):
        try:
            return AccessRoleRule.objects.get(pk=pk)
        except AccessRoleRule.DoesNotExist:
            return None

    @admin_required
    def patch(self, request, pk):
        rule = self._get_rule(pk)
        if not rule:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccessRoleRuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin_required
    def delete(self, request, pk):
        rule = self._get_rule(pk)
        if not rule:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
