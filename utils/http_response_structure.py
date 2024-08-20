from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


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
