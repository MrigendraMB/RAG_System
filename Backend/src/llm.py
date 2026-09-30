import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer(question, context_chunks):
    # Build context string from chunks
    context = "\n\n".join(context_chunks)
    
    # Build prompt
    system_prompt = f"""You are a helpful legal assistant for Nepal Labour Law. 
Answer the question using ONLY the provided context.
If the answer is not in the context, say 'I don't know based on the provided legal documents.'
Always be concise and clear.

Context:
{context}"""
    
    models_to_try = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "llama-3.1-8b-instant"]
    
    for model_name in models_to_try:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "temperature": 0.5,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ]
                },
                timeout=30
            )
            data = response.json()
            if response.status_code == 200 and "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling Groq API model {model_name}: {e}")
            continue
            
    return "Unable to generate an answer right now. Please verify your Groq API configuration."

