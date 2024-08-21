import os
import requests
from rest_framework import status
from app.adapters.adapters import DataSource
from utils.http_response_structure import general_response


class ApiGoAnyWhereAdapter(DataSource):
    def __init__(self, proceso: str, data: dict = None):
        self.data = data
        self.auth = (os.getenv("WEB_USER_GAW"), os.getenv("WEB_USER_PASS_GAW"))
        self.api_url = os.getenv("URL_SECURITY_FORM_GAW").replace(
            "$%PROCESO%$", proceso
        )

    def obtener_vendedores(self):
        try:
            response_payload = requests.get(self.api_url, auth=self.auth)
            response_payload.raise_for_status()
            response_payload_json = response_payload.json()
            api_url_form = response_payload_json.get("data", {}).get("submitFormLink")

            if api_url_form:
                response = requests.post(api_url_form, json=self.data, auth=self.auth)
                response.raise_for_status()
                response_json = response.json()
                return response_json.get("data", {}).get("message", "")

        except Exception:
            raise general_response(
                status.HTTP_400_BAD_REQUEST, False, "Ha ocurrido un error inesperado"
            )
