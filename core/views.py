import json
from requests import HTTPError
from app.adapters.adapters import DataSource
from rest_framework import status
from authentication.authentication import TokenValidate
from utils.http_response_structure import general_response
from app.adapters.goanywhere_adapter import ApiGoAnyWhereAdapter
from rest_framework.decorators import api_view, authentication_classes


# @swagger_auto_schema(
#     method="get",
#     tags=["Excelencia en Distribucion"],
#     operation_description="Endpoint para obtener los vendedores asignados a un supervisor.",
#     responses={status.HTTP_200_OK: ResponseApiSerializer},
# )
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_vendedores_supervisor(request, codigo_supervisor):
    def process_data(data_source: DataSource):
        return data_source.obtener_vendedores()

    try:
        body = {"codigoSupervisor": codigo_supervisor}
        api_adapter = ApiGoAnyWhereAdapter("busquedaVendedores", body)
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


# @swagger_auto_schema(
#     method="get",
#     tags=["Excelencia en Distribucion"],
#     operation_description="Endpoint para obtener la planeacion de un vendedor por clientes.",
#     responses={status.HTTP_200_OK: ResponseApiSerializer},
# )
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_planeacion_vendedor_cliente(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_planeacion_vendedor_cliente()

    try:
        body = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("planificacion_cliente_vendededor", body)
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


# @swagger_auto_schema(
#     method="get",
#     tags=["Excelencia en Distribucion"],
#     operation_description="Endpoint para obtener la cuota grabada y el total planeado de un vendedor.",
#     responses={status.HTTP_200_OK: ResponseApiSerializer},
# )
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_cuota_grabada_planeado(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_cuota_grabada_planeado()

    try:
        body = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("busquedaCuotaGrabadaPlaneada", body)
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


# @swagger_auto_schema(
#     method="put",
#     tags=["Excelencia en Distribucion"],
#     operation_description="Endpoint para guardar la planeación del vendedor.",
#     responses={status.HTTP_201_CREATED: ResponseApiSerializer},
# )
@api_view(["PUT"])
@authentication_classes([TokenValidate])
def guardar_planeacion_vendedor(request):
    def process_data(data_source: DataSource):
        return data_source.guardar_planeacion_vendedor()

    try:
        body = json.loads(request.body.decode("utf-8"))
        api_adapter = ApiGoAnyWhereAdapter("guardar_planeacion_vendedor_cliente", body)
        process_data(api_adapter)
        return general_response(status.HTTP_200_OK, True, "Operación exitosa")
    except HTTPError:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
    except Exception:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
        )
