import cProfile
import pstats
from typing import Dict
from dotenv import load_dotenv
import psycopg2.extras
import uuid
from psycopg2.extras import Json
import psycopg2
from MetadataRepository import MetadataRepository
from psycopg2 import sql
import datetime
import os


class PostgresService(MetadataRepository):
    def __init__(self, connstring):
        self.conn = psycopg2.connect(connstring)
        self.conn.autocommit = True
        psycopg2.extras.register_uuid()
    
        load_dotenv()
        self.table = os.getenv("DATA_TABLE")

    def save(self, filename: str, metadata: Dict, storage_key: str) -> None:
        insert_query = 'insert into {} (id, filename, metadata, fileloc) values %s'.format(sql.Identifier(self.table))

        row = (uuid.uuid4(), filename, Json(metadata), storage_key, datetime.datetime.now())

        with self.conn.cursor() as curs:
            curs.execute(insert_query, (row,))


    def query(self, metadata:Dict) -> list:
        query =  """
            SELECT * 
            FROM {}
            WHERE metadata @> %s;
            """.format(sql.Identifier(self.table))
        
        with self.conn.cursor() as curs:
            curs.execute(query ,[Json(metadata),])
            result = curs.fetchmany(5)
            return result
        
            

    def batchInsert(self, data):
     
        with self.conn.cursor() as curs:
            insert_query = sql.SQL('insert into {table} (id, filename, fileloc, metadata, timestamp_added) values %s').format(table=sql.Identifier(self.table))
            rows = PostgresService.formatRows(data)
            
            psycopg2.extras.execute_values (
            curs, insert_query, rows, template=None
            )


    def formatRows(data: list):
        return ((uuid.uuid4(), "no_filename", "no_loc", Json(d), datetime.datetime.now())
                        for d in data )