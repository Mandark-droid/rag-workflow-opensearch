from opensearchpy import OpenSearch, RequestsHttpConnection
from config import OPENSEARCH_HOST, OPENSEARCH_INDEX,OPENSEARCH_USER, OPENSEARCH_PORT,OPENSEARCH_PASS

# Initialize OpenSearch client
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_compress=False,
    http_auth=(OPENSEARCH_USER, OPENSEARCH_PASS),
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    connection_class=RequestsHttpConnection,
    timeout=30
)


def create_index(index_name=OPENSEARCH_INDEX, dims=384):
    if not client.indices.exists(index=index_name):
        mapping = {
    "settings": {
        "index": {
            "knn": True,
            "number_of_shards": 1,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "timestamp": {
                "type": "date"
            },
            "content": {"type": "text"},
            "content_vector": {
                "type": "knn_vector",
                "dimension": dims,
                "method": {
                    "name": "hnsw",
                    "engine": "lucene",
                    "space_type": "l2"
                }
            }
        }
    }
}
        client.indices.create(index=index_name, body=mapping)


def index_document(doc_id, document, index_name=OPENSEARCH_INDEX):
    client.index(index=index_name, id=doc_id, body=document)


def delete_document(doc_id, index_name=OPENSEARCH_INDEX):
    client.delete(index=index_name, id=doc_id, ignore=[404])


def vector_search(query_vector, k=5, index_name=OPENSEARCH_INDEX):
    body = {
        "size": k,
        "query": {
            "knn": {
                "content_vector": {
                    "vector": query_vector,
                    "k": k
                }
            }
        }
    }
    resp = client.search(index=index_name, body=body)
    return resp['hits']['hits']
