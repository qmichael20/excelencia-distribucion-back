import os
import requests
from utils.utils import string_to_json
from app.adapters.adapters import DataSource


class ApiGoAnyWhereAdapter(DataSource):
    def __init__(self, proceso: str, data: dict | list = None):
        self.data = data
        self.proceso = proceso

    def obtener_codigo_supervisor_por_correo(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_codigo_vendedor_por_credenciales(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_vendedores(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_cuota_grabada_planeado_clientes(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_planeacion_vendedor_cliente(self):
        return consumir_formulario(self.proceso, self.data)

    def guardar_planeacion_vendedor_cliente(self):
        guardar_planeacion_vendedor(self)

    def obtener_cuota_grabada_planeado_proveedores(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_planeacion_vendedor_proveedor(self):
        return consumir_formulario(self.proceso, self.data)

    def guardar_planeacion_vendedor_proveedor(self):
        guardar_planeacion_vendedor(self)

    def aprobar_planeacion_vendedor(self):
        if isinstance(self.data["data"], list):
            for element in self.data["data"]:
                body = armar_body(self.proceso, element)
                consumir_formulario(self.data["proceso_auxiliar"], body)

        return consumir_formulario(
            self.proceso, {"codigoVendedor": self.data["codigoVendedor"]}
        )

    def obtener_resumen_planeacion_clientes(self):
        return consumir_formulario(self.proceso, self.data)

    def obtener_resumen_planeacion_proveedores(self):
        return consumir_formulario(self.proceso, self.data)


def guardar_planeacion_vendedor(self):
    if isinstance(self.data, list):
        for element in self.data:
            body = armar_body(self.proceso, element)
            consumir_formulario(self.proceso, body)


def armar_body(proceso: str, data: dict):
    if "proveedor" in proceso:
        return {
            "codigoVendedor": data["vendedor"],
            "codigoProveedor": data["codigoProveedor"],
            "planeacion": str(data["planeacion"]),
        }
    else:
        return {
            "codigoVendedor": data["vendedor"],
            "codigoCliente": data["codigoCliente"],
            "planeacion": str(data["planeacion"]),
        }


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
