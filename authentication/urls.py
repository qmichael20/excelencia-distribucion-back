from django.urls import path
from .views import autenticar_por_jwt, refresh_token

urlpatterns = [
    path("validar_token/", autenticar_por_jwt, name="validar_token"),
    path("refresh_token/", refresh_token, name="refresh_token"),
]
