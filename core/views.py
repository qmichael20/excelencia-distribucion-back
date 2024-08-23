from requests import HTTPError
from app.adapters.adapters import DataSource
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from utils.http_response_structure import general_response
from authentication.serializers import ResponseApiSerializer
from app.adapters.goanywhere_adapter import ApiGoAnyWhereAdapter
from rest_framework.decorators import api_view, permission_classes


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener los vendedores asignados a un supervisor.",
    responses={200: ResponseApiSerializer},
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def obtener_vendedores_supervisor(request, codigo_supervisor):
    def process_data(data_source: DataSource):
        return data_source.obtener_vendedores()

    try:
        headers = {"codigoSupervisor": codigo_supervisor}
        api_adapter = ApiGoAnyWhereAdapter("busquedaVendedores", headers)
        data = process_data(api_adapter)
        return general_response(status.HTTP_200_OK, True, "Operación exitosa", data)
    except HTTPError:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
    except Exception:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener la planeacion de un vendedor por clientes.",
    responses={200: ResponseApiSerializer},
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def obtener_planeacion_vendedor_cliente(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_planeacion_vendedor_cliente()

    try:
        headers = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("planificacion_cliente_vendededor", headers)
        data = process_data(api_adapter)
        return general_response(status.HTTP_200_OK, True, "Operación exitosa", data)
    except HTTPError:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
    except Exception:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener la cuota grabada y el total planeado de un vendedor.",
    responses={200: ResponseApiSerializer},
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def obtener_cuota_grabada_planeado(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_cuota_grabada_planeado()

    try:
        headers = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("busquedaCuotaGrabadaPlaneada", headers)
        data = process_data(api_adapter)
        return general_response(status.HTTP_200_OK, True, "Operación exitosa", data)
    except HTTPError:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
    except Exception:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
