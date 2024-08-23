from django.urls import re_path
from core.views import (
    obtener_vendedores_supervisor,
    obtener_cuota_grabada_planeado,
    obtener_planeacion_vendedor_cliente,
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
        r"^planificacion_cliente_vendededor/(?P<codigo_vendedor>\w+)/$",
        obtener_planeacion_vendedor_cliente,
        name="planificacion_cliente_vendededor",
    ),
]
