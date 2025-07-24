from MockDataCreator import MockDataCreator

from services.PostgresService import PostgresService
from services.MinioService import MinioService
from services.FileUploadService import FileUploadService
from tqdm import tqdm
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    
    MINIO_USERNAME = os.getenv('MINIO_USERNAME')
    MINIO_HOST=os.getenv("MINIO_HOST")
    MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
    POSTGRES_CONN = os.getenv("POSTGRES_CONN")
    print(POSTGRES_CONN)

    s3_service = MinioService(MINIO_HOST, MINIO_USERNAME, MINIO_PASSWORD, bucket_name="test-data-lake-bucket" )
    pg_service = PostgresService(POSTGRES_CONN)
    upload_service = FileUploadService(storage=s3_service,
                                       metadata_repo=pg_service)


    metadatas = list(MockDataCreator.take_n(MockDataCreator.create_metadata(), 2))
    for metadata in tqdm(metadatas):
        upload_service.upload("test.txt", None, metadata)







