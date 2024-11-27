import secrets
from rest_framework import serializers
from .models import Token, Resource
from django.utils.timezone import now, timedelta

from .selectors import get_token_from_headers


class TokenSerializer(serializers.ModelSerializer):
    expires_at = serializers.CharField(read_only=True)

    class Meta:
        model = Token
        fields = [
            "token",
            "is_revoked",
            "scope",
            "created_at",
            "expires_at",
        ]
        read_only_fields = ["token", "created_at"]

    def create(self, validated_data):
        expiration_time = now() + timedelta(hours=24)
        token = secrets.token_urlsafe(32)
        return Token.objects.create(
            resource=self.context["resource"],
            token=token,
            expires_at=expiration_time,
            scope=validated_data.get("scope", None),
        )


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "name", "url", "created_at"]
        read_only_fields = ["identifier", "api_key", "created_at"]


class RevokeTokenSerializer(serializers.Serializer):
    apikey = serializers.CharField(required=True)
    identifier = serializers.CharField(required=True)

    class Meta:
        fields = ("apikey", "identifier")

    def validate(self, data):
        apikey = data.get("apikey")
        identifier = data.get("identifier")
        token_value = self.context.get("token")
        try:
            token_instance = Token.objects.get(token=token_value, is_revoked=False)
        except Token.DoesNotExist:
            raise serializers.ValidationError("Invalid or already revoked token.")

        try:
            resource = Resource.objects.get(api_key=apikey, identifier=identifier)
        except Resource.DoesNotExist:
            raise serializers.ValidationError("Invalid apikey or identifier.")

        data["token"] = token_instance
        return data
