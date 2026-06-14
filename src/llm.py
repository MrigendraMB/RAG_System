import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer(question, context_chunks):
    # Build context string from chunks
    context = "\n\n".join(context_chunks)
    
    # Build prompt
    system_prompt = f"""You are a helpful assistant. 
    Answer the question using ONLY the provided context.
    If the answer is not in the context, say 'I don't know'.
    Always be concise.

Context:
{context}"""
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        }
    )
    
    data = response.json()
    return data["choices"][0]["message"]["content"]
