from gnews import GNews
import time
from gnewsdecoder import gnewsdecoder
from gnewsdecoder import decode
google_news = GNews(language='en', period='1h', max_results=2)
seen_hashes = set()

def track_gnews(query):
    articles = google_news.get_news(query)
    new_articles = [a for a in articles if hash(a['title']) not in seen_hashes]
    
    for article in new_articles:
        print(f"🚨 NEW: {article['title']}")
        print(f"📅 {article['published date']}")
        print(f"{article['description']}")
        print(f"🔗 {article['url']}\n")
        print(f" {article['publisher']}\n")
        
        decode(article['url'])
        
    print("--------------------------------")
    print("--------------------------------")


if __name__ == "__main__":
    user_query = input("Enter your news query: ")
    start_time = time.time()
    track_gnews(user_query)
    elapsed = time.time() - start_time
    print(f"\n⏱️ Results delivered in {elapsed:.5f} seconds.")