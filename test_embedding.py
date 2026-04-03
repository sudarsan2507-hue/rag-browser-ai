from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Machine learning is a subset of AI",
    "What is ML?",
    "I love playing football"
]

# Convert to embeddings
embeddings = model.encode(sentences)

# Compare similarity
sim_1_2 = cosine_similarity([embeddings[0]], [embeddings[1]])
sim_1_3 = cosine_similarity([embeddings[0]], [embeddings[2]])

print("Similarity (ML vs Machine Learning):", sim_1_2[0][0])
print("Similarity (ML vs Football):", sim_1_3[0][0])