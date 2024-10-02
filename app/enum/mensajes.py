from enum import Enum


# Definición del enum de tipos de mensajes
class Mensajes(Enum):
    CRED_INVALIDAS = "Credenciales invalidas."
    ERROR_INESPERADO = "Error inesperado."
    TOKEN_INVALIDO = "El token proporcionado es inválido."
    OPERACION_EXITOSA = "Operación exitosa."
    REFRESH_TOKEN_REQUERIDO = "Refresh token es requerido."
    TOKEN_EXPERIDADO = "El token proporcionado es inválido o ha expirado."
