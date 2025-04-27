import os

# OpenSearch settings
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = os.getenv("OPENSEARCH_PORT", "9200")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "rag-pipeline-index")
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASS = os.getenv("OPENSEARCH_PASS", "admin")

# Embedding model (Sentence-Transformers)
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2"
)

# Hugging Face LLM model for generation
default_hf = "kshitijthakkar/qwen2_5-Coder-1_5b-loggenix-2k_merged"
HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", default_hf)
HF_DEVICE = os.getenv("HF_DEVICE", "cpu")  # "cpu" or "cuda"

# Folder to watch for ingestion
data_folder = os.getenv("DATA_FOLDER", "./watched_folder")
