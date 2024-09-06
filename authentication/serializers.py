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
