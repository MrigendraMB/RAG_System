import chromadb
import os
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents")

def store_chunks(chunks, embeddings, source_file):
    filename = os.path.basename(source_file)
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_file, "filename": filename} for _ in chunks]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    return metadatas
    

def search(query_embedding, n_results=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results


def delete_document_chunks(filename):
    try:
        source_file = f"data/{filename}"
        # Delete by filename metadata or source
        collection.delete(where={"filename": filename})
        return True
    except Exception as e:
        print(f"Error deleting chunks for {filename}: {e}")
        try:
            collection.delete(where={"source": f"data/{filename}"})
            return True
        except Exception as ex:
            print(f"Fallback delete failed: {ex}")
            return False

