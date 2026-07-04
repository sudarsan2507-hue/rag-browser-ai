import sys
from playwright.sync_api import sync_playwright
from interface.cli import get_query
from browser.navigator import search_google
from retrieval.extractor import fetch_all
from retrieval.chunker import chunk_text
from rag.embedder import embed_chunks

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    query = get_query()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        results = search_google(page, query)
        records = fetch_all(page, results)

        browser.close()

    print(f"\nFetched {len(records)} pages:\n")

    all_chunks = []
    chunk_counts = []

    for r in records:
        chunks = chunk_text(r["content"])
        chunk_counts.append(len(chunks))
        all_chunks.extend(chunks)

    embeddings = embed_chunks(all_chunks)
    print(f"Embedded {len(all_chunks)} chunks -> vectors of dimension {embeddings.shape[1]}\n")

    offset = 0
    for i, (r, count) in enumerate(zip(records, chunk_counts), 1):
        preview = all_chunks[offset][:200].replace("\n", " ") if count else ""

        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print(f"   {len(r['content'])} chars extracted -> {count} chunks")
        print(f"   Chunk 1 preview: {preview}...\n")
        offset += count

if __name__ == "__main__":
    main()
