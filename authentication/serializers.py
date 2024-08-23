import re
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["codigoSupervisor"] = "001"
        token["tipoUsuario"] = "supervisor"
        return token


class ResponseApiSerializer(serializers.Serializer):
    message = serializers.CharField()
    statusCode = serializers.IntegerField()
    token = TokenSerializer()
    data = serializers.JSONField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta(object):
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ya está en uso.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "La contraseña debe tener al menos 6 caracteres."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un número."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula."
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un carácter especial."
            )
        return value
