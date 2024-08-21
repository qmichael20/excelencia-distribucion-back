from django.urls import re_path
from .views import login, signup, test_token, refresh_token

urlpatterns = [
    re_path("login/", login, name="login"),
    re_path("signup/", signup, name="signup"),
    re_path("test/", test_token, name="signup"),
    re_path("refresh_token/", refresh_token, name="signup"),
]
