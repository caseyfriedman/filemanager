from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def store(self, filename: str, contents: bytes) -> str:
        pass