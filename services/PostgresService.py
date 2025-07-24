from typing import Dict
import psycopg2.extras
import uuid
from psycopg2.extras import Json
import psycopg2
from MetadataRepository import MetadataRepository

class PostgresService(MetadataRepository):
    def __init__(self, connstring):
        self.conn = psycopg2.connect(connstring)
        self.conn.autocommit = True
        psycopg2.extras.register_uuid()

    def save(self, filename: str, metadata: Dict, storage_key: str) -> None:
        insert_query = 'insert into integration_test (id, filename, metadata, fileloc) values %s'

        row = (uuid.uuid4(), filename, Json(metadata), storage_key)

        with self.conn.cursor() as curs:
            curs.execute(insert_query, (row,))


    def query(self, metadata:Dict) -> list:
        query =  """
            SELECT * 
            FROM testtable 
            WHERE metadata @> %s;
            """
        
        with self.conn.cursor() as curs:
            curs.execute(query ,[Json(metadata),])
            result = curs.fetchmany(5)
            return result
        
            

    def batchInsert(self, data):
        with self.conn.cursor() as curs:
            insert_query = 'insert into testtable (id, filename, metadata) values %s'
            rows = ((uuid.uuid4(), d['filename'], Json(d['metadata']))
                        for d in data )
            psycopg2.extras.execute_values (
            curs, insert_query, rows, template=None
            )
