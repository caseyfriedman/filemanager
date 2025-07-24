from MetadataRepository import MetadataRepository
from opensearchpy import OpenSearch, helpers

class OpensearchService(MetadataRepository):

    def __init__(self):
        self.client = OpenSearch(
            hosts = [{'host': 'localhost', 'port': 9200}],
            http_compress = True, # enables gzip compression for request bodies
            use_ssl = False,
            verify_certs = False,
        )

    def batchInsert(self, data):
        actions = [
                {
        "_index": "my-index",
        "_source": doc
            }
            for doc in data
        ]

        helpers.bulk(self.client, actions)