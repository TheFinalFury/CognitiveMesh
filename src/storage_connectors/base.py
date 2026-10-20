from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseStorageConnector(ABC):
    """Abstract interface for all non-relational database connectors."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the storage engine."""
        pass

    @abstractmethod
    def ping(self) -> bool:
        """Verify connection health status."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Safely close active connections and pools."""
        pass
