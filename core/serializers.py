from rest_framework import serializers
from core.models import Vendedor


class VendedorSerializer(serializers.ModelSerializer):
    vendedor = serializers.CharField(required=True)

    class Meta:
        model = Vendedor
        fields = ["vendedor"]


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ResponseApiSerializer(serializers.Serializer):
    message = serializers.CharField()
    statusCode = serializers.IntegerField()
    token = TokenSerializer()
    data = serializers.JSONField()
