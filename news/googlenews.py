from GoogleNews import GoogleNews
import time

def track_news(query, interval_minutes=30):
    googlenews = GoogleNews(lang='en', period='1h')
    last_seen = set()  # Track already seen headlines
    
    print(f"Checking news for '{query}'...")
    googlenews.clear()
    googlenews.search(query)
    new_results = googlenews.results()
        
    for article in new_results:
        if article['title'] not in last_seen:
            print(f"📰 New: {article['title']}\n🔗 {article['link']}\n")
            last_seen.add(article['title'])
        

# Start tracking (e.g., 'AI news')
track_news('pope')
