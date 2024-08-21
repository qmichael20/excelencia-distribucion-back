from authentication import serializers
from core.models import Vendedor


class VendedorSerializer(serializers.ModelSerializer):
    vendedor = serializers.CharField(required=True)

    class Meta:
        model = Vendedor
        fields = ["vendedor"]
