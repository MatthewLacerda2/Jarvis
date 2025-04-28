from gnews import GNews

google_news = GNews(language='en', period='1h', max_results=20)
seen_hashes = set()

def track_gnews(query):

    articles = google_news.get_news(query)
    new_articles = [a for a in articles if hash(a['title']) not in seen_hashes]
    
    for article in new_articles:
        print(f"🚨 NEW: {article['title']}")
        print(f"📅 {article['published_date']}")
        print(f"{article['description']}")
        print(f"🔗 {article['url']}\n")
        print(f" {article['publisher']}\n")
        seen_hashes.add(hash(article['title']))

track_gnews('bitcoin')
