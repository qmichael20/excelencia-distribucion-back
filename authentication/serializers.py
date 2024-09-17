from authentication.models import Usuarios
from rest_framework import serializers


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = "__all__"


class UserAutenticatedSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    display_name = serializers.CharField(max_length=100)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ResponseApiSerializer(serializers.Serializer):
    message = serializers.CharField()
    statusCode = serializers.IntegerField()
    data = serializers.JSONField()
    token = TokenSerializer(required=False)


class RefreshTokenSerializer(serializers.Serializer):
    Refresh = serializers.CharField(required=True, help_text="Token de refresco válido")
