import pymongo
from MetadataRepository import MetadataRepository

class MongoService(MetadataRepository):


    def __init__(self, connection_string):
        self.mongoClient = pymongo.MongoClient(connection_string)

    def batchInsert(self, data):
        db = self.mongoClient.test1
        collection=db.newcollection
        collection.insert_many(data, ordered=False)