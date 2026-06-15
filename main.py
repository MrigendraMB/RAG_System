import sys
sys.path.append("src")

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ingestion import process_pdf
from embeddings import embedding
from retrieval import store_chunks, search
from llm import generate_answer

app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    processed_chunks = process_pdf(file_path)
    embeddings = embedding(processed_chunks)
    store_chunks(processed_chunks, embeddings, file_path)
    return {"message": f"Successfully processed {file.filename}", "chunks": len(processed_chunks)}

@app.post("/ask")
async def ask_question(question: str):
    query_embedding = embedding([question])[0]
    results = search(query_embedding, n_results=5)
    if not results["documents"][0]:
        return {"answer": "No documents uploaded yet. Please upload a PDF first."}
    context_chunks = results["documents"][0]
    answer = generate_answer(question, context_chunks)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)