from django.urls import re_path
from core.views import obtener_vendedores_supervisor

urlpatterns = [
    re_path(
        r"^vendedores/(?P<codigo_supervisor>\w+)/$",
        obtener_vendedores_supervisor,
        name="vendedores_por_supervisor",
    )
]
