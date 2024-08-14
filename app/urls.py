from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
]
