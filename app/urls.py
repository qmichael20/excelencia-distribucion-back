from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Excelencia en distribucion API",
        default_version="v1",
        description="Descripción de la API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="meico@meico.com.co"),
        license=openapi.License(name="Licencia"),
    ),
    public=True,
)
urlpatterns = [
    path("api/auth/", include("authentication.urls")),
    path("api/planeacion/", include("core.urls")),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
