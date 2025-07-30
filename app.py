import os
import time

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import redis
from flask import Flask, jsonify

from models.FileEntry import FileEntry
from services.MinioService import MinioService
from flask import request

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379)

load_dotenv()
    
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_CONN")
db = SQLAlchemy()


db.init_app(app)

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
    query_metadata = {}
    for key, value in request.args.items():
        query_metadata[key] = value

    results = db.session.query(FileEntry).filter(FileEntry.metadata_.contains(query_metadata)).limit(25).all()
    results = db.session.query(FileEntry).filter(getattr(FileEntry, "filename") == "no_filename").limit(25).all()
    return results

    
@app.route('/upload')
def initialize():
   s3_service = MinioService(bucket_name="my-app-bucket")