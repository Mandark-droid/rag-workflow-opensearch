from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME
import numpy as np

# Load embedding model
embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def normalize_vector(vector):
    return vector / np.linalg.norm(vector)

def generate_embedding(text: str):
    # returns a Python list of floats
    embedding = embed_model.encode(str(text))
    embedding = normalize_vector(embedding).tolist()
    return embedding
