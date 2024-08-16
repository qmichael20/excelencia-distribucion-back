from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from authentication.serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers


def general_response(status, success, message, token=None, data=None):
    response_data = {
        "statusCode": status,
        "success": success,
        "message": message,
    }

    if token:
        response_data["token"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }

    if data is not None:
        response_data["data"] = data

    return Response(response_data, status=status)


def invalid_credentials_response():
    return Response(
        {
            "statusCode": status.HTTP_401_UNAUTHORIZED,
            "success": False,
            "message": "Las credenciales proporcionadas son invalidas.",
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


def success_response(token, data):
    return Response(
        {
            "statusCode": status.HTTP_200_OK,
            "success": True,
            "message": "Operacion exitosa",
            "token": {
                "refresh": str(token),
                "access": str(token.access_token),
            },
            "data": data,
        },
        status=status.HTTP_200_OK,
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ResponseApi(serializers.Serializer):
    message = serializers.CharField()
    statusCode = serializers.IntegerField()
    token = TokenSerializer()
    data = serializers.JSONField()


@swagger_auto_schema(
    method="post",
    tags=["Autenticación"],
    responses={200: ResponseApi},
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
    responses={200: ResponseApi},
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
        "Operacion fallida",
        None,
        user_serializer.errors,
    )


@swagger_auto_schema(
    method="get",
    tags=["Autenticación"],
    responses={200: ResponseApi},
    security=[{"Bearer": []}],
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
