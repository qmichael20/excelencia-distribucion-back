import json
from requests import HTTPError
from app.adapters.adapters import DataSource
from rest_framework import status
from authentication.authentication import TokenValidate
from authentication.serializers import ResponseApiSerializer
from utils.http_response_structure import general_response
from app.adapters.goanywhere_adapter import ApiGoAnyWhereAdapter
from rest_framework.decorators import api_view, authentication_classes
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener los vendedores asignados a un supervisor.",
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
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


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener la cuota grabada y el total planeado de un vendedor por clientes.",
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_cuota_grabada_planeado_clientes(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_cuota_grabada_planeado_clientes()

    try:
        body = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("busquedaCuotaGrabadaPlaneadaClientes", body)
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
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_planeacion_vendedor_cliente(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_planeacion_vendedor_cliente()

    try:
        body = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("planeacion_cliente_vendededor", body)
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
    method="put",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para guardar la planeación del vendedor.",
    responses={status.HTTP_201_CREATED: ResponseApiSerializer},
)
@api_view(["PUT"])
@authentication_classes([TokenValidate])
def guardar_planeacion_vendedor_cliente(request):
    def process_data(data_source: DataSource):
        return data_source.guardar_planeacion_vendedor_cliente()

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


@swagger_auto_schema(
    method="get",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para obtener la cuota grabada y el total planeado de un vendedor por proveedores.",
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_cuota_grabada_planeado_proveedores(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_cuota_grabada_planeado_proveedores()

    try:
        body = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter(
            "busquedaCuotaGrabadaPlaneadaProveedores", body
        )
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
    operation_description="Endpoint para obtener la planeacion de un vendedor por proveedores.",
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["GET"])
@authentication_classes([TokenValidate])
def obtener_planeacion_vendedor_proveedor(request, codigo_vendedor):
    def process_data(data_source: DataSource):
        return data_source.obtener_planeacion_vendedor_proveedor()

    try:
        body = {"codigoVendedor": codigo_vendedor}
        api_adapter = ApiGoAnyWhereAdapter("planeacion_cliente_proveedor", body)
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
    method="put",
    tags=["Excelencia en Distribucion"],
    operation_description="Endpoint para guardar la planeación del vendedor - proveedor.",
    responses={status.HTTP_201_CREATED: ResponseApiSerializer},
)
@api_view(["PUT"])
@authentication_classes([TokenValidate])
def guardar_planeacion_vendedor_proveedor(request):
    def process_data(data_source: DataSource):
        return data_source.guardar_planeacion_vendedor_proveedor()

    try:
        body = json.loads(request.body.decode("utf-8"))
        api_adapter = ApiGoAnyWhereAdapter(
            "guardar_planeacion_vendedor_proveedor", body
        )
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
