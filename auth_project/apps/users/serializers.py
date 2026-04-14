from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "middle_name", "email",
                  "is_active", "role_name", "created_at", "updated_at"]
        read_only_fields = ["id", "is_active", "role_name", "created_at", "updated_at"]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name", "email"]

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
