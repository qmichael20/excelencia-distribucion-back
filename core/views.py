from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from authentication.serializers import ResponseApiSerializer
from core.adapters import DataSource
from gaw.gaw_adapter import ApiGoAnyWhereAdapter
from utils.http_response_structure import general_response
from utils.utils import string_to_json


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener los vendedores asignados a un supervisor.",
    responses={200: ResponseApiSerializer},
)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def obtener_vendedores_supervisor(request, codigo_supervisor):
    def process_data(data_source: DataSource):
        return data_source.fetch_data()

    try:
        headers = {"codigoSupervisor": codigo_supervisor}
        api_adapter = ApiGoAnyWhereAdapter("busquedaVendedores", headers)
        data = process_data(api_adapter)
        return general_response(
            status.HTTP_200_OK, True, "Operación exitosa", string_to_json(data)
        )
    except Exception:
        raise general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
