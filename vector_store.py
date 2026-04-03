import chromadb
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize DB
client = chromadb.Client()
collection = client.create_collection(name="my_knowledge")

# Data
documents = [
    "Machine learning is a subset of AI",
    "Artificial Intelligence is powerful",
    "Football is a popular sport"
]

# Store data
embeddings = model.encode(documents)
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=["1", "2", "3"]
)

# 🔥 QUERY PART (NEW)
query = "What is ML?"

query_embedding = model.encode([query])

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print("Query:", query)
print("Results:", results['documents'])