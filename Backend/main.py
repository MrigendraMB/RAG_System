import sys
import os
from typing import Optional
sys.path.append("src")

from fastapi import FastAPI, UploadFile, File, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from ingestion import process_pdf
from embeddings import embedding
from retrieval import store_chunks, search, delete_document_chunks
from llm import generate_answer

app = FastAPI(title="Kanoon Saathi API", version="1.0")

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

@app.get("/documents")
async def list_documents():
    data_dir = "data"
    docs = []
    if os.path.exists(data_dir):
        for fname in os.listdir(data_dir):
            fpath = os.path.join(data_dir, fname)
            if os.path.isfile(fpath):
                stat = os.stat(fpath)
                docs.append({
                    "name": fname,
                    "filename": fname,
                    "category": "Legal Document",
                    "status": "Processed",
                    "size": stat.st_size,
                    "mtime": stat.st_mtime
                })
    # Sort documents by modification time descending (latest first)
    docs.sort(key=lambda d: d["mtime"], reverse=True)
    return {"documents": docs}

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    fpath = os.path.join("data", filename)
    file_deleted = False
    if os.path.exists(fpath):
        os.remove(fpath)
        file_deleted = True
    chunks_deleted = delete_document_chunks(filename)
    return {"message": f"Deleted {filename}", "file_deleted": file_deleted, "chunks_deleted": chunks_deleted}

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
        
    context_items = []
    for doc, meta in zip(documents, metadatas):
        src = meta.get("source", "Unknown")
        fn = meta.get("filename") or os.path.basename(src)
        context_items.append({"doc": doc, "source": src, "filename": fn, "metadata": meta})
        
    answer, cited_filenames = generate_answer(q, context_items)

    # Return metadata for ONLY the specific source document(s) actually cited
    matched_metadatas = []
    seen = set()
    for c_fn in cited_filenames:
        for meta in metadatas:
            src = meta.get("source", "")
            m_fn = meta.get("filename") or os.path.basename(src)
            if (c_fn.lower() == m_fn.lower() or c_fn.lower() in m_fn.lower() or m_fn.lower() in c_fn.lower()) and m_fn not in seen:
                seen.add(m_fn)
                matched_metadatas.append(meta)
                break

    return {"answer": answer, "citations": matched_metadatas}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
