from abc import ABC
from minio import Minio
import uuid
import os.path

class MinioService(ABC):

    def __init__(self,  host, username, password, bucket_name ):
        self.client = Minio(host,
        access_key=username,
        secret_key=password,
        secure=False
    )
        
        self.bucket = bucket_name


    def store(self, filename: str, contents: bytes) -> str:
        return self.upload(filename)

    def uploadFile(self, bucket_name, as_filename, filepath):
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
    
        self.client.fput_object(bucket_name, as_filename, filepath)


    def downloadFile(self, bucket_name, path, filename):
        result = self.client.fget_object(bucket_name, filename,  path)
    
    @staticmethod
    def generateUniqueFilename():
        unique_id = uuid.uuid4()
        filename = f"{unique_id}"
        return filename

    def upload(self, filename):
        unique_filename = MinioService.generateUniqueFilename()
        data_lake_storage_path = "/data-lake-storage"
        hashnumber = int(unique_filename[-1], 16) % 16
        hashfolder = f"hash_{hashnumber}"

        loc_ref = os.path.join(hashfolder,unique_filename)
        objectname = os.path.join(data_lake_storage_path, loc_ref)
        self.uploadFile(self.bucket, objectname, filename)
        return loc_ref