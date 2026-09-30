from ingestion import process_pdf
from sentence_transformers import CrossEncoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
def rerank(question, chunks, top_k=5):
    scores = []
    for chunk in chunks:
        score = reranker.predict([(question, chunk)])
        # pair each chunk with its score
        scores.append(score)

    chunk_scores = list(zip(scores, chunks))    
    # sort by score, highest first
    chunk_scores.sort(reverse=True)
    # take top_k chunks
    top_chunks = [chunk for score, chunk in chunk_scores[:top_k]]
    # sort chunks by score, highest first
    return top_chunks

if __name__ == "__main__":
    test_chunks = [
        "The Child Labour Act was enacted in 1956 by the government",
        "No child who has not completed eighteen years of age shall be employed",
        "Child labour inspectors visit factories regularly for compliance checks"
    ]
    result = rerank("is child labor legal?", test_chunks, top_k=2)
    print(result)