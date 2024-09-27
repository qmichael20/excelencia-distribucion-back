from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def obtener_vendedores(self):
        pass

    @abstractmethod
    def obtener_cuota_grabada_planeado_clientes(self):
        pass

    @abstractmethod
    def obtener_planeacion_vendedor_cliente(self):
        pass

    @abstractmethod
    def guardar_planeacion_vendedor_cliente(self):
        pass

    @abstractmethod
    def obtener_cuota_grabada_planeado_proveedores(self):
        pass

    @abstractmethod
    def obtener_planeacion_vendedor_proveedor(self):
        pass

    @abstractmethod
    def guardar_planeacion_vendedor_proveedor(self):
        pass

    @abstractmethod
    def aprobar_planeacion_vendedor(self):
        pass

    @abstractmethod
    def obtener_resumen_planeacion_clientes(self):
        pass

    @abstractmethod
    def obtener_resumen_planeacion_proveedores(self):
        pass
