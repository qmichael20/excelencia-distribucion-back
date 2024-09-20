import jwt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from authentication.authentication import AllowAnonymous
from authentication.serializers import RefreshTokenSerializer, ResponseApiSerializer
from utils.http_response_structure import general_response, success_response
from .services import generar_token_from_refresh, validar_jwt_msal, generar_token
from drf_yasg.utils import swagger_auto_schema


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
            tokens = generar_token(user_data)
            return success_response(tokens, user_data)
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El token proporcionado es inválido.",
        )
    except jwt.ExpiredSignatureError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El token proporcionado es inválido.",
        )
    except jwt.InvalidTokenError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El token proporcionado es inválido.",
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
            status.HTTP_400_BAD_REQUEST, False, "Refresh token es requerido."
        )

    try:
        return generar_token_from_refresh(refresh_token)
    except jwt.ExpiredSignatureError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El token proporcionado es inválido.",
        )
    except jwt.InvalidTokenError:
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El token proporcionado es inválido.",
        )
