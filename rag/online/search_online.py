from googlesearch import search

query = "Python tutorials"
results = search(query, num_results=20, advanced=True)
for result in results:
    print(f"\nTitle: {result.title}")
    print(f"URL: {result.url}")
    print(f"Description: {result.description}")
    print("-" * 50)
