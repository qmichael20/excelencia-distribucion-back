from rest_framework.response import Response
from rest_framework import status
from typing import TypeVar, Optional

T = TypeVar("T")


class Token:
    def __init__(self, refresh: str, access: str):
        self.refresh = refresh
        self.access_token = access


def general_response(
    status: status,
    success: bool,
    message: str,
    data: Optional[T] = None,
    token: Optional[Token] = None,
):
    response_data = {
        "statusCode": status,
        "success": success,
        "message": message,
    }

    if token:
        response_data["token"] = {
            "refresh": token.get("refresh"),
            "access": token.get("access"),
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
            "data": data,
            "token": {
                "refresh": token.get("refresh"),
                "access": token.get("access"),
            },
        },
        status=status.HTTP_200_OK,
    )
