import time
from urllib.parse import urlparse
from retrieval.cleaner import extract_readability

FETCH_DELAY_SECONDS = 1


def fetch_page_content(page, url):
    scheme = urlparse(url).scheme
    if scheme not in ("http", "https"):
        raise ValueError(f"unsupported URL scheme: {scheme!r}")

    page.goto(url, wait_until="domcontentloaded", timeout=15000)
    html = page.content()
    return extract_readability(html)


def fetch_all(page, results):
    records = []

    for i, r in enumerate(results):
        if i > 0:
            time.sleep(FETCH_DELAY_SECONDS)

        try:
            content = fetch_page_content(page, r["link"])
        except Exception as e:
            print(f"Skipped {r['link']}: {e}")
            continue

        records.append({
            "title": r["title"],
            "url": r["link"],
            "content": content
        })

    return records
