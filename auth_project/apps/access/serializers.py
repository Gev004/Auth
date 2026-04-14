from rest_framework import serializers
from .models import Role, BusinessElement, AccessRoleRule


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = "__all__"


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)
    element_name = serializers.CharField(source="element.name", read_only=True)

    class Meta:
        model = AccessRoleRule
        fields = "__all__"
