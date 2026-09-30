import sys
import os
from typing import Optional
sys.path.append("src")

from fastapi import FastAPI, UploadFile, File, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from ingestion import process_pdf
from embeddings import embedding
from retrieval import store_chunks, search
from llm import generate_answer

app = FastAPI(title="Kanoon Saathi API", version="2.0")

# Enable CORS for Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{file.filename}"
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    processed_chunks = process_pdf(file_path)
    embeddings = embedding(processed_chunks)
    store_chunks(processed_chunks, embeddings, file_path)
    return {"message": f"Successfully processed {file.filename}", "chunks": len(processed_chunks)}

@app.post("/ask")
async def ask_question(request: Request, question: Optional[str] = Query(None)):
    q = question
    if not q:
        try:
            body = await request.json()
            if isinstance(body, dict):
                q = body.get("question")
        except Exception:
            pass
            
    if not q:
        return {"answer": "Please provide a question.", "citations": []}

    query_embedding = embedding([q])[0]
    results = search(query_embedding, n_results=5)
    
    documents = results.get("documents", [[]])[0] if results.get("documents") else []
    metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
    
    if not documents:
        return {"answer": "No documents uploaded yet. Please upload a PDF first.", "citations": []}
        
    context_chunks = [
        f"[Source: {meta.get('source', 'Unknown')}]\n{doc}" 
        for doc, meta in zip(documents, metadatas)
    ]
    answer = generate_answer(q, context_chunks)
    return {"answer": answer, "citations": metadatas}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)