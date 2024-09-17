import os
import jwt
from django.utils import timezone
from datetime import timedelta
from typing import Optional, Dict, Any
from utils.http_response_structure import success_response


def obtener_llave_publica_msal(token: str) -> Dict[str, Any]:
    jwks_client = jwt.PyJWKClient(os.getenv("JWKS_URI"))
    rsa_key = jwks_client.get_signing_key_from_jwt(token).key
    return rsa_key


def validar_jwt_msal(token: str) -> Optional[Dict[str, Any]]:
    try:
        public_key = obtener_llave_publica_msal(token)
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=[os.getenv("ALGORITHM")],
            audience=os.getenv("CLIENT_ID"),
            issuer=os.getenv("ISSUER"),
        )
        return {
            "user_name": decoded_token.get("preferred_username"),
            "display_name": decoded_token.get("name"),
            "email": decoded_token.get("preferred_username"),
        }
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError


def generar_token(user_data: Dict[str, Any]) -> Dict[str, str]:
    secret = os.getenv("SECRET")
    algorithm = os.getenv("ALGORITHM_TOKEN")

    access_payload = {
        "user_name": user_data.get("user_name"),
        "email": user_data.get("email"),
        "display_name": user_data.get("display_name"),
        "tipoUsuario": "supervisor",
        "codigoSupervisor": "004",
        # "codigoVendedor": "N21",
        "exp": timezone.now()
        + timedelta(hours=int(os.getenv("ACCESS_TOKEN_EXPIRATION"))),
    }

    access_token = jwt.encode(access_payload, secret, algorithm=algorithm)

    refresh_payload = {
        "user_name": user_data.get("user_name"),
        "email": user_data.get("email"),
        "display_name": user_data.get("display_name"),
        "tipoUsuario": "supervisor",
        "codigoSupervisor": "004",
        # "codigoVendedor": "N21",
        "exp": timezone.now()
        + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRATION"))),
    }

    refresh_token = jwt.encode(refresh_payload, secret, algorithm=algorithm)

    return {"access": access_token, "refresh": refresh_token}


def generar_token_from_refresh(refresh_token: str) -> Dict[str, str]:
    secret = os.getenv("SECRET")
    algorithm = os.getenv("ALGORITHM_TOKEN")

    try:
        refresh_payload = jwt.decode(refresh_token, secret, algorithms=algorithm)
        token = generar_token(refresh_payload)
        return success_response(token, refresh_payload)
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError
