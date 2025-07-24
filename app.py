import os
import time

from dotenv import load_dotenv
import redis
from flask import Flask, jsonify

from MockDataCreator import MockDataCreator
from services.PostgresService import PostgresService
from services.MinioService import MinioService
from services.FileUploadService import FileUploadService
from flask import request

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379)

load_dotenv()
    
POSTGRES_CONN = os.getenv("POSTGRES_CONN")

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'

@app.route('/query')
def query():
    svc = PostgresService(POSTGRES_CONN)
    metadata = {}
    for key, value in request.args.items():
        metadata[key] = value
    
    return svc.query(metadata)

    
@app.route('/upload')
def initialize():
   s3_service = MinioService(bucket_name="my-app-bucket")