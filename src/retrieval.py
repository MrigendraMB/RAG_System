import chromadb

# create a client
client = chromadb.Client()

# create a collection (like a table in SQL)
collection = client.create_collection("documents")

# add documents
collection.add(
    documents=["chunk text here"],
    embeddings=[[0.1, 0.2, 0.3, ...]],
    metadatas=[{"source": "file.pdf", "page": 1}],
    ids=["chunk_1"]
)

# search
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3, ...]],
    n_results=5
)