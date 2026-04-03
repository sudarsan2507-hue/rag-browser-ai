from browser.navigator import search_google   # from your Phase 1
import chromadb
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Init DB
client = chromadb.Client()
collection = client.create_collection(name="rag_data")

# Step 1: Get search results
query = "What is Machine Learning?"
results = search_google(query)

# Extract only titles (simplify for now)
documents = [r['title'] for r in results]

# Step 2: Store in DB
embeddings = model.encode(documents)

collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(documents))]
)

# Step 3: Query again (simulate user)
new_query = "Explain ML"

query_embedding = model.encode([new_query])

response = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print("User Query:", new_query)
print("Best Matches:", response['documents'])