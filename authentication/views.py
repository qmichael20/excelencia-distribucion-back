from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.models import User
from authentication.serializers import (
    LoginSerializer,
    ResponseApiSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_yasg.utils import swagger_auto_schema
from utils.http_response_structure import (
    general_response,
    invalid_credentials_response,
    success_response,
)


@swagger_auto_schema(
    method="post",
    tags=["Autenticación"],
    operation_description="Endpoint para login de usuarios.",
    responses={200: ResponseApiSerializer},
    request_body=LoginSerializer,
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    user = User.objects.filter(email=request.data["email"]).first()

    if not user:
        return invalid_credentials_response()

    if not user.check_password(request.data["password"]):
        return invalid_credentials_response()

    token = CustomTokenObtainPairSerializer.get_token(user)
    user_serializer = UserSerializer(instance=user)

    return success_response(token, user_serializer.data)


@swagger_auto_schema(
    method="post",
    tags=["Autenticación"],
    responses={200: ResponseApiSerializer},
    request_body=UserSerializer,
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(request.data["password"])
        user.save()
        token = CustomTokenObtainPairSerializer.get_token(user)
        return success_response(token, user_serializer.data)

    return general_response(
        status.HTTP_400_BAD_REQUEST,
        False,
        "Ha ocurrido un error inesperado",
        user_serializer.errors,
    )


@swagger_auto_schema(
    method="get", tags=["Autenticación"], responses={200: ResponseApiSerializer}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def test_token(request):
    user = request.user
    token = CustomTokenObtainPairSerializer.get_token(user)
    user_serializer = UserSerializer(instance=user)
    return success_response(token, user_serializer.data)


@swagger_auto_schema(method="post", tags=["Autenticación"])
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return general_response(
            status.HTTP_400_BAD_REQUEST, False, "Refresh token es requerido."
        )

    try:
        token = RefreshToken(refresh_token)
        user_id = token["user_id"]
        user = User.objects.get(id=user_id)
        token = CustomTokenObtainPairSerializer.get_token(user)
        user_serializer = UserSerializer(instance=user)
        return success_response(token, user_serializer.data)

    except (InvalidToken, TokenError):
        return general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El refresh token proporcionado es invalido.",
        )
    except User.DoesNotExist:
        return general_response(
            status.HTTP_404_NOT_FOUND, False, "Usuario no encontrado."
        )
