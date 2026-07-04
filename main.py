import sys
from playwright.sync_api import sync_playwright
from interface.cli import get_query
from browser.navigator import search_google
from retrieval.extractor import fetch_all

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

    for i, r in enumerate(records, 1):
        preview = r["content"][:300].replace("\n", " ")
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print(f"   {len(r['content'])} chars extracted")
        print(f"   Preview: {preview}...\n")

if __name__ == "__main__":
    main()