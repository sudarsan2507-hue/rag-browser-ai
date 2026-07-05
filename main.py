import sys
from playwright.sync_api import sync_playwright
from interface.cli import get_query
from browser.navigator import search_google, launch_browser
from retrieval.extractor import fetch_all
from retrieval.chunker import chunk_text
from rag.embedder import embed_chunks
from rag.vector_store import add_chunks
from rag.retriever import retrieve
from llm.generator import generate_answer, ensure_ollama_ready

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ensure_ollama_ready()
    query = get_query()

    with sync_playwright() as p:
        browser = launch_browser(p)
        page = browser.new_page()

        try:
            results = search_google(page, query)
        except Exception as e:
            print(f"Search failed: {e}")
            results = []

        records = fetch_all(page, results) if results else []
        browser.close()

    print(f"\nFetched {len(records)} pages:\n")

    records_chunks = [(r, chunk_text(r["content"])) for r in records]

    all_chunks = [c for _, chunks in records_chunks for c in chunks]
    metadatas = [
        {"title": r["title"], "url": r["url"]}
        for r, chunks in records_chunks
        for _ in chunks
    ]

    if not all_chunks:
        print("No content could be extracted from any result. Try a different query.")
        return

    embeddings = embed_chunks(all_chunks)
    print(f"Embedded {len(all_chunks)} chunks -> vectors of dimension {embeddings.shape[1]}\n")

    add_chunks(all_chunks, embeddings, metadatas)
    print(f"Stored {len(all_chunks)} chunks in the persistent vector store.\n")

    for i, (r, chunks) in enumerate(records_chunks, 1):
        preview = chunks[0][:200].replace("\n", " ") if chunks else ""

        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print(f"   {len(r['content'])} chars extracted -> {len(chunks)} chunks")
        print(f"   Chunk 1 preview: {preview}...\n")

    retrieved = retrieve(query, k=3)
    answer = generate_answer(query, retrieved)

    print("Answer:\n")
    print(answer)
    print("\nSources:")
    for i, (_, meta, _distance) in enumerate(retrieved, 1):
        print(f"  [{i}] {meta['title']} - {meta['url']}")

if __name__ == "__main__":
    main()
