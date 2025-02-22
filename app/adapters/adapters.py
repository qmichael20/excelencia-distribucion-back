from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def obtener_vendedores(self):
        pass

    @abstractmethod
    def obtener_cuota_grabada_planeado(self):
        pass

    @abstractmethod
    def obtener_planeacion_vendedor_cliente(self):
        pass

    @abstractmethod
    def guardar_planeacion_vendedor(self):
        pass
