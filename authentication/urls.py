from django.urls import path
from .views import (
    autenticar_por_jwt,
    refresh_token,
    autenticar_por_credenciales_celuweb,
)

urlpatterns = [
    path(
        "validar_credenciales/",
        autenticar_por_credenciales_celuweb,
        name="validar_credenciales",
    ),
    path("validar_token/", autenticar_por_jwt, name="validar_token"),
    path("refresh_token/", refresh_token, name="refresh_token"),
]
