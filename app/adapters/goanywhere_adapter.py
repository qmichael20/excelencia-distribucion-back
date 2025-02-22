import os
import requests
from utils.utils import string_to_json
from app.adapters.adapters import DataSource


class ApiGoAnyWhereAdapter(DataSource):
    def __init__(self, proceso: str, data: dict | list = None):
        self.data = data
        self.proceso = proceso

    def obtener_vendedores(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_cuota_grabada_planeado(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_planeacion_vendedor_cliente(self):
        return consumir_formulario(self.proceso, self.data)

    def guardar_planeacion_vendedor(self):
        if isinstance(self.data, list):
            for element in self.data:
                if element["aprobado"] is True:
                    body = {
                        "codigoVendedor": element["vendedor"],
                        "codigoCliente": element["codigoCliente"],
                        "planeacion": str(element["planeacion"]),
                        "aprobado": "true",
                    }
                    consumir_formulario(self.proceso, body)
                else:
                    body = {
                        "codigoVendedor": element["vendedor"],
                        "codigoCliente": element["codigoCliente"],
                        "planeacion": str(element["planeacion"]),
                    }
                    consumir_formulario(self.proceso, body)


def consumir_formulario(proceso: str, data: dict = None):
    auth = (os.getenv("WEB_USER_GAW"), os.getenv("WEB_USER_PASS_GAW"))
    api_url = os.getenv("URL_FORM_GAW").replace("$%PROCESO%$", proceso)

    try:
        response_payload = requests.get(api_url, auth=auth)
        response_payload.raise_for_status()
        response_payload_json = response_payload.json()
        api_url_form = response_payload_json.get("data", {}).get("submitFormLink")

        if api_url_form:
            response = requests.post(api_url_form, json=data, auth=auth)
            response.raise_for_status()
            response_json = response.json()
            data = response_json.get("data", {}).get("message", "")
            if isinstance(data, str):
                return string_to_json(data)

        raise requests.HTTPError

    except requests.HTTPError:
        raise requests.HTTPError
