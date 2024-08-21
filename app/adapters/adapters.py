from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def obtener_vendedores(self):
        """Fetch data from the source."""
        pass
