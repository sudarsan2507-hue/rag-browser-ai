import uuid
import chromadb

client = chromadb.PersistentClient(path="chroma_data")
collection = client.get_or_create_collection(name="rag_data")


def add_chunks(chunks, embeddings, metadatas, target_collection=None):
    target_collection = target_collection or collection
    ids = [str(uuid.uuid4()) for _ in chunks]
    target_collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )


def search(query_embedding, n_results=3, target_collection=None):
    target_collection = target_collection or collection
    return target_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )


if __name__ == "__main__":
    from rag.embedder import embed_chunks

    demo_collection = client.get_or_create_collection(name="demo_data")

    documents = [
        "Machine learning is a subset of AI",
        "Artificial Intelligence is powerful",
        "Football is a popular sport"
    ]
    metadatas = [{"source": "demo"}] * len(documents)

    add_chunks(documents, embed_chunks(documents), metadatas, target_collection=demo_collection)

    query = "What is ML?"
    query_embedding = embed_chunks([query])[0]
    results = search(query_embedding, n_results=2, target_collection=demo_collection)

    print("Query:", query)
    print("Results:", results["documents"])
