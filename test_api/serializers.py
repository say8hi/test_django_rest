from rest_framework import serializers
import re
from .models import User, Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["user_id", "id_type", "password"]
        read_only_fields = ["id_type"]

    def validate_user_id(self, value):
        if re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", value):
            return value
        elif re.match(r"^\d+$", value):
            return value
        else:
            raise serializers.ValidationError(
                "User ID must be a valid email or phone number."
            )

    def create(self, validated_data):
        user_id = validated_data["user_id"]
        password = validated_data["password"]

        if "@" in user_id:
            id_type = "email"
        else:
            id_type = "phone"

        user = User.objects.create_user(
            user_id=user_id, password=password, id_type=id_type
        )
        return user


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ["token"]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "id_type"]
