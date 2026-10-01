import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer(question, context_items):
    """
    context_items: list of dicts with keys 'doc', 'source', 'filename'
    Returns: (answer_str, cited_filenames_list)
    """
    formatted_chunks = []
    for idx, item in enumerate(context_items, 1):
        fn = item.get("filename") or os.path.basename(item.get("source", "Legal Document"))
        formatted_chunks.append(f"--- Document Chunk {idx} [Source: {fn}] ---\n{item.get('doc', '')}")
    
    context = "\n\n".join(formatted_chunks)
    
    system_prompt = f"""You are a helpful legal assistant for Nepal Labour Law.
Answer the question using ONLY the provided context chunks.

FORMATTING & STRUCTURE INSTRUCTIONS:
- Whenever presenting lists, comparisons, working hours, leave rules, or structured legal data, format them using clean Markdown tables (e.g. | Topic | Detail |) or Mermaid diagrams (```mermaid ... ```) for maximum clarity.

CRITICAL INSTRUCTION FOR CITATIONS:
- Identify ONLY the specific document chunk(s) that directly contain the facts used in your answer.
- At the very end of your response, on a new line, list ONLY the source filename(s) (e.g. Nepal_Labour_Act_2074.pdf) from which your answer was derived.
- Format the source line exactly as:
SOURCES: filename1.pdf, filename2.pdf

If the answer is not in the context, say 'I don't know based on the provided legal documents.' and write:
SOURCES: None

Context:
{context}"""
    
    models_to_try = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "llama-3.1-8b-instant"]
    
    raw_response = None
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
                    "temperature": 0.3,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ]
                },
                timeout=30
            )
            data = response.json()
            if response.status_code == 200 and "choices" in data and len(data["choices"]) > 0:
                raw_response = data["choices"][0]["message"]["content"]
                break
        except Exception as e:
            print(f"Error calling Groq API model {model_name}: {e}")
            continue
            
    if not raw_response:
        return "Unable to generate an answer right now. Please verify your Groq API configuration.", []

    answer = raw_response
    cited_filenames = []

    if "SOURCES:" in raw_response:
        parts = raw_response.rsplit("SOURCES:", 1)
        answer = parts[0].strip()
        sources_str = parts[1].strip()
        if sources_str.lower() != "none":
            for src in sources_str.split(","):
                cleaned = src.strip().strip("'\"`[]()")
                if cleaned and cleaned.lower() != "none":
                    cited_filenames.append(cleaned)

    # Validate against actual retrieved context filenames
    valid_filenames = list(dict.fromkeys(
        item.get("filename") or os.path.basename(item.get("source", ""))
        for item in context_items if item.get("filename") or item.get("source")
    ))

    matched = []
    for c in cited_filenames:
        for vf in valid_filenames:
            if c.lower() == vf.lower() or c.lower() in vf.lower() or vf.lower() in c.lower():
                if vf not in matched:
                    matched.append(vf)

    # Fallback if SOURCES wasn't generated properly but answer was provided
    if not matched and "don't know" not in answer.lower():
        # Include first retrieved document filename as fallback
        if valid_filenames:
            matched.append(valid_filenames[0])

    return answer, matched


