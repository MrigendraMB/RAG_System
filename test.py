import sys
sys.path.append('src')
from retrieval import collection

print("Total chunks in database:", collection.count())

# get all unique sources
all_data = collection.get()
sources = set()
for meta in all_data['metadatas']:
    sources.add(meta['source'])

print("Unique sources:", sources)