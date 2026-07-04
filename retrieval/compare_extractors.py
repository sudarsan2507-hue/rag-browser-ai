import sys
import trafilatura
from playwright.sync_api import sync_playwright
from retrieval.cleaner import extract_paragraphs, extract_readability

# Same 5 URLs returned by the Phase 2 test run, fixed here for apples-to-apples comparison.
URLS = [
    "https://www.w3schools.com/python/",
    "https://www.geeksforgeeks.org/python/python-programming-language-tutorial/",
    "https://docs.python.org/3/tutorial/index.html",
    "https://www.tutorialspoint.com/python/index.htm",
    "https://www.learnpython.org/",
]


def extract_trafilatura(html):
    return trafilatura.extract(html) or ""


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        for url in URLS:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                html = page.content()
            except Exception as e:
                print(f"Skipped {url}: {e}")
                continue

            homemade = extract_paragraphs(html, max_link_density=0.5)
            readability_text = extract_readability(html)
            trafilatura_text = extract_trafilatura(html)

            print(f"\n{url}")
            print(f"  homemade (<p> + link-density): {len(homemade)} chars")
            print(f"  readability-lxml:              {len(readability_text)} chars")
            print(f"  trafilatura:                    {len(trafilatura_text)} chars")
            print(f"  readability preview: {readability_text[:300].replace(chr(10), ' ')}...")
            print(f"  trafilatura preview: {trafilatura_text[:300].replace(chr(10), ' ')}...")

        browser.close()


if __name__ == "__main__":
    main()
