import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import HF_MODEL_NAME, HF_DEVICE
from embedder import generate_embedding
from opensearch_utils import vector_search

# Load HF model & tokenizer
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(HF_MODEL_NAME)
# Move model to specified device
device = torch.device(HF_DEVICE if torch.cuda.is_available() and HF_DEVICE == 'cuda' else 'cpu')
model.to(device)
# device = "cpu"
# model.to(device)


def answer_query(user_query: str, k=5, max_new_tokens=512):
    # 1. Retrieve similar docs
    query_vec = generate_embedding(user_query)
    hits = vector_search(query_vec, k)
    context = "\n---\n".join([hit['_source']['content'] for hit in hits])

    # 2. Build prompt
    prompt = (
        f"You are an expert assistant. Use the following documents to answer the question. "
        f"\n\nDocuments: \n{context}\n\nQuestion: {user_query}\nAnswer: "
    )

    # 3. Tokenize & generate
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract answer part
    return reply.split("Answer:")[-1].strip()


if __name__ == '__main__':
    query = input("Enter your question: ")
    print(answer_query(query))
