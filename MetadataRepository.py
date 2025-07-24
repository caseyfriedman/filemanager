from abc import ABC, abstractmethod
from typing import Dict

class MetadataRepository(ABC):
    @abstractmethod
    def save(self, filename: str, metadata: Dict, storage_key: str) -> None:
        ...