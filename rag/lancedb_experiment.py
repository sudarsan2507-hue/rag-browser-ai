import lancedb
from rag.embedder import embed_chunks

db = lancedb.connect("lancedb_data")

documents = [
    "Machine learning is a subset of AI",
    "Artificial Intelligence is powerful",
    "Football is a popular sport"
]
metadatas = [{"source": "demo"}] * len(documents)


def add_demo_data():
    embeddings = embed_chunks(documents)
    data = [
        {"text": doc, "vector": emb, **meta}
        for doc, emb, meta in zip(documents, embeddings, metadatas)
    ]
    return db.create_table("demo_data", data=data, mode="overwrite")


def query_demo(query_text, n_results=2):
    table = db.open_table("demo_data")
    query_embedding = embed_chunks([query_text])[0]
    return table.search(query_embedding).limit(n_results).to_list()


if __name__ == "__main__":
    add_demo_data()

    query = "What is ML?"
    results = query_demo(query)

    print("Query:", query)
    for r in results:
        print(f"  {r['text']!r} (distance={r['_distance']:.4f})")
