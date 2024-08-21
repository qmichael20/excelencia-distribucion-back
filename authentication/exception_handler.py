from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from utils.http_response_structure import general_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed):
        response = general_response(
            status.HTTP_401_UNAUTHORIZED,
            False,
            "El token proporcionado es inválido o ha expirado.",
        )
    return response
