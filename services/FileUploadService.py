
from typing import Dict
from services.FilestoreService import FileStorage
from MetadataRepository import MetadataRepository


class FileUploadService:
    def __init__(self,
                 storage: FileStorage,
                 metadata_repo: MetadataRepository):
        self.storage = storage
        self.repo = metadata_repo

    def upload(self, filename: str, contents: bytes, metadata: Dict) -> None:
        storage_key = self.storage.store(filename, contents)
        self.repo.save(filename, metadata, storage_key)