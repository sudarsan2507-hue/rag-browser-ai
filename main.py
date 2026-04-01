from interface.cli import get_query
from browser.navigator import search_google

def main():
    query = get_query()
    results = search_google(query)

    print("\nTop Results:\n")

    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['link']}\n")

if __name__ == "__main__":
    main()