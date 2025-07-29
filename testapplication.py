from MockDataCreator import MockDataCreator

from services.PostgresService import PostgresService
from services.MinioService import MinioService
from services.FileUploadService import FileUploadService
from tqdm import tqdm
from dotenv import load_dotenv
import os
import cProfile, pstats
from io import StringIO

load_dotenv()

MINIO_USERNAME = os.getenv('MINIO_USERNAME')
MINIO_HOST=os.getenv("MINIO_HOST")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
POSTGRES_CONN = os.getenv("POSTGRES_CONN")


def testEndpoint():

    s3_service = MinioService(MINIO_HOST, MINIO_USERNAME, MINIO_PASSWORD, bucket_name="test-data-lake-bucket")
    pg_service = PostgresService(POSTGRES_CONN)
    upload_service = FileUploadService(storage=s3_service,
                                       metadata_repo=pg_service)

    metadatas = list(MockDataCreator.take_n(MockDataCreator.create_metadata(), 2))
    for metadata in tqdm(metadatas):
        upload_service.upload("test.txt", None, metadata)

def testBulkInsertion(total):
    pg_service = PostgresService(POSTGRES_CONN)
    batch_size = 10000

    with tqdm(total=total) as pbar:
        for batch in MockDataCreator.batcher(MockDataCreator.take_n(MockDataCreator.create_metadata(), total), batch_size=batch_size):

            pg_service.batchInsert(batch)
            pbar.update(batch_size)


if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()
    testBulkInsertion(50_000)      # or whatever total you like
    pr.disable()


    stats = pstats.Stats(pr).strip_dirs().sort_stats("cumtime")
    stats.print_stats("batchInsert")      # shows ncalls, tottime, percall for inserts
    stats.print_stats("create_metadata")  # shows stats for your generator
    stats.print_stats("execute_values")
    stats.print_stats("formatRows")


