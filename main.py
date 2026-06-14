import sys
sys.path.append("src")
if __name__ == "__main__":
    from ingestion import process_pdf
    from embeddings import embedding
    from retrieval import store_chunks, search
    from llm import generate_answer
    # Step 1: Process PDF and get chunks
    pdf_path = "D:\\Projects\\rag_system\\data\\test.pdf"
    chunks = process_pdf(pdf_path)
    
    # Step 2: Generate embeddings for the chunks
    embeddings = embedding(chunks)
    
    # Step 3: Store chunks and embeddings in ChromaDB
    store_chunks(chunks, embeddings, pdf_path)
    
    # Step 4: Test search functionality
    query = "Give me detail about Cross-Border Protocol Limitations?"
    query_embedding = embedding([query])[0]
    results = search(query_embedding, n_results=2)
    # Step 5: Generate answer using the retrieved chunks
    retrieved_chunks = results["documents"][0]
    answer = generate_answer(query, retrieved_chunks)

    print("Generated Answer:")
    print(answer)