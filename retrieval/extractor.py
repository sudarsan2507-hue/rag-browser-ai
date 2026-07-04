from retrieval.cleaner import extract_readability


def fetch_page_content(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=15000)
    html = page.content()
    return extract_readability(html)


def fetch_all(page, results):
    records = []

    for r in results:
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
