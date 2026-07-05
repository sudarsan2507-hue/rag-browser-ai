from rag.embedder import embed_chunks
from rag.vector_store import search


def retrieve(query, k=3, where=None):
    query_embedding = embed_chunks([query])[0]
    results = search(query_embedding, n_results=k, where=where)

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return list(zip(chunks, metadatas, distances))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    for query in ["budget gaming laptop", "how do python for loops work"]:
        print(f"\nQuery: {query!r}")

        for chunk, meta, distance in retrieve(query, k=3):
            preview = chunk[:120].replace("\n", " ")
            print(f"  [{distance:.4f}] {meta['title']}")
            print(f"           {preview}...")
