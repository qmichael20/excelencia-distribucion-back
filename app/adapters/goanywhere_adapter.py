import os
import requests
from utils.utils import string_to_json
from app.adapters.adapters import DataSource


class ApiGoAnyWhereAdapter(DataSource):
    def __init__(self, proceso: str, data: dict = None):
        self.data = data
        self.auth = (os.getenv("WEB_USER_GAW"), os.getenv("WEB_USER_PASS_GAW"))
        self.api_url = os.getenv("URL_FORM_GAW").replace("$%PROCESO%$", proceso)

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
                data = response_json.get("data", {}).get("message", "")
                if isinstance(data, str):
                    return string_to_json(data)

            raise requests.HTTPError

        except requests.HTTPError:
            raise requests.HTTPError
