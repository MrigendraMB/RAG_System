import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
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
