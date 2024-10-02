import jwt
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from app.adapters.adapters import DataSource
from app.adapters.goanywhere_adapter import ApiGoAnyWhereAdapter
from app.enum.mensajes import Mensajes
from app.enum.tipo_usuario import TipoUsuarios
from authentication.authentication import AllowAnonymous
from authentication.serializers import RefreshTokenSerializer, ResponseApiSerializer
from utils.http_response_structure import general_response, success_response
from .services import generar_token_from_refresh, validar_jwt_msal, generar_token
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="post",
    tags=["Autenticación"],
    operation_description="Endpoint para validar usuarios con credenciales celuweb.",
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAnonymous])
def autenticar_por_credenciales_celuweb(request):
    credenciales = request.data.get("credenciales")

    try:
        api_adapter = ApiGoAnyWhereAdapter(
            "obtener_codigo_vendedor_por_credenciales", credenciales
        )
        data = process_data(api_adapter)

        if isinstance(data, list) and data[0]["codigo"] is not None:
            user_data = {
                "codigoVendedor": data[0]["codigo"],
                "tipoUsuario": TipoUsuarios.VENDEDOR.value,
            }
            tokens = generar_token(user_data)
            return success_response(tokens, user_data)

        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            Mensajes.CRED_INVALIDAS.value,
        )
    except requests.HTTPError:
        return general_response(
            status.HTTP_400_BAD_REQUEST,
            False,
            Mensajes.ERROR_INESPERADO.value,
        )
    except Exception:
        return general_response(
            status.HTTP_400_BAD_REQUEST,
            False,
            Mensajes.ERROR_INESPERADO.value,
        )


@swagger_auto_schema(
    method="post",
    tags=["Autenticación"],
    operation_description="Endpoint para validar el token de microsoft.",
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAnonymous])
def autenticar_por_jwt(request):
    token = request.data.get("token")
    try:
        user_data = validar_jwt_msal(token)
        if user_data is not None:
            body = {"correo": user_data["email"]}
            api_adapter = ApiGoAnyWhereAdapter(
                "obtener_codigo_supervisor_por_correo", body
            )
            data = process_data(api_adapter)

            if isinstance(data, list) and data[0]["codigo"] is not None:
                user_data["codigoSupervisor"] = data[0]["codigo"]
                user_data["tipoUsuario"] = TipoUsuarios.SUPERVISOR.value
                tokens = generar_token(user_data)
                return success_response(tokens, user_data)

        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            Mensajes.TOKEN_INVALIDO.value,
        )
    except jwt.ExpiredSignatureError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            Mensajes.TOKEN_INVALIDO.value,
        )
    except jwt.InvalidTokenError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            Mensajes.TOKEN_INVALIDO.value,
        )


@swagger_auto_schema(
    method="post",
    tags=["Autenticación"],
    operation_description="Endpoint para refrescar el token de la app.",
    request_body=RefreshTokenSerializer,
    responses={status.HTTP_200_OK: ResponseApiSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAnonymous])
def refresh_token(request):
    refresh_token = request.headers.get("Refresh")

    if not refresh_token:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, Mensajes.REFRESH_TOKEN_REQUERIDO.value
        )

    try:
        return generar_token_from_refresh(refresh_token)
    except jwt.ExpiredSignatureError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            Mensajes.TOKEN_INVALIDO.value,
        )
    except jwt.InvalidTokenError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            Mensajes.TOKEN_INVALIDO.value,
        )


def process_data(data_source: DataSource):
    return data_source.obtener_codigo_supervisor_por_correo()
