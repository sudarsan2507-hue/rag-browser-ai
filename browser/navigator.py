from playwright.sync_api import sync_playwright

def search_google(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        # DuckDuckGo search
        page.goto(f"https://duckduckgo.com/?q={query}")

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

        browser.close()

    return results