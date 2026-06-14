import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("documents")

def store_chunks(chunks, embeddings, source_file):
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_file} for _ in chunks]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    

def search(query_embedding, n_results=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results


if __name__ == "__main__":
    from embeddings import embedding
    
    test_chunks = [
        "Nepal is a beautiful country in South Asia",
        "Machine learning is a subset of artificial intelligence",
        "RAG systems retrieve relevant documents before generating answers"
    ]
    
    # generate embeddings
    embeddings = embedding(test_chunks)
    
    # store in chroma
    store_chunks(test_chunks, embeddings, "test.pdf")
    
    # search
    query = "What is RAG?"
    query_embedding = embedding([query])[0]
    results = search(query_embedding, n_results=2)
    
    print(results)