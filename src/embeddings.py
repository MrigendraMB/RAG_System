from sentence_transformers import SentenceTransformer 
model = SentenceTransformer('all-MiniLM-L6-v2')  

def embedding(chunks):  
    embeddings = model.encode(chunks)
    return embeddings

if __name__ == "__main__":
    test_chunks = [
        "Nepal is a beautiful country",
        "Machine learning is a subset of AI",
        "RAG systems use vector databases"
    ]
    embeddings = embedding(test_chunks)
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")