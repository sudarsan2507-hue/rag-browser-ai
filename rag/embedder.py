from sentence_transformers import SentenceTransformer

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def embed_chunks(chunks):
    return _get_model().encode(chunks, normalize_embeddings=True)


if __name__ == "__main__":
    from sklearn.metrics.pairwise import cosine_similarity

    sentences = [
        "Machine learning is a subset of AI",
        "What is ML?",
        "I love playing football"
    ]

    embeddings = embed_chunks(sentences)

    sim_1_2 = cosine_similarity([embeddings[0]], [embeddings[1]])
    sim_1_3 = cosine_similarity([embeddings[0]], [embeddings[2]])

    print("Similarity (ML vs Machine Learning):", sim_1_2[0][0])
    print("Similarity (ML vs Football):", sim_1_3[0][0])
