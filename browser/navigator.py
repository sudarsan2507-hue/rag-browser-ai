import os
from urllib.parse import quote_plus


def launch_browser(playwright):
    headless = os.environ.get("RAG_HEADLESS", "false").lower() == "true"
    slow_mo = int(os.environ.get("RAG_SLOW_MO", "100"))
    return playwright.chromium.launch(headless=headless, slow_mo=slow_mo)


def search_google(page, query):
    results = []

    # DuckDuckGo search
    page.goto(f"https://duckduckgo.com/?q={quote_plus(query)}")

    # WAIT for results
    page.wait_for_selector("a[data-testid='result-title-a']")

    # GET elements
    elements = page.query_selector_all("a[data-testid='result-title-a']")

    for el in elements[:5]:
        title = el.inner_text()
        link = el.get_attribute("href")

        results.append({
            "title": title,
            "link": link
        })

    return results
