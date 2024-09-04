from django.urls import re_path
from core.views import (
    obtener_vendedores_supervisor,
    obtener_cuota_grabada_planeado,
    obtener_planeacion_vendedor_cliente,
    guardar_planeacion_vendedor,
)

urlpatterns = [
    re_path(
        r"^vendedores/(?P<codigo_supervisor>\w+)/$",
        obtener_vendedores_supervisor,
        name="vendedores_por_supervisor",
    ),
    re_path(
        r"^cuota_grabada_planeado/(?P<codigo_vendedor>\w+)/$",
        obtener_cuota_grabada_planeado,
        name="obtener_cuota_grabada_planeado",
    ),
    re_path(
        r"^obtener_planeacion_vendedor_cliente/(?P<codigo_vendedor>\w+)/$",
        obtener_planeacion_vendedor_cliente,
        name="obtener_planeacion_vendedor_cliente",
    ),
    re_path(
        "guardar_planeacion_vendedor_cliente/",
        guardar_planeacion_vendedor,
        name="guardar_planeacion_vendedor_cliente",
    ),
]
