import os
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


class TokenValidate(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        token = auth_header.replace("Bearer ", "")
        secret = os.getenv("SECRET")
        algorithm = os.getenv("ALGORITHM_TOKEN")

        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])
            return (payload, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed()
        except jwt.InvalidTokenError:
            raise AuthenticationFailed()
        except Exception:
            raise AuthenticationFailed()


class AllowAnonymous(BasePermission):
    def has_permission(self, request, view):
        return True
