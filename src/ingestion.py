import fitz

def extract_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)
    return chunks

def process_pdf(pdf_path):
    print(f"Processing: {pdf_path}")
    text = extract_text(pdf_path)
    chunks = chunk_text(text)
    
    return chunks
