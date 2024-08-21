from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def fetch_data(self):
        """Fetch data from the source."""
        pass
