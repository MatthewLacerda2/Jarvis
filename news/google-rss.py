import feedparser
from datetime import datetime, timedelta
import time

def track_rss(query):
    url = f"https://news.google.com/rss/search?q={query}+when:1h&ceid=US:en"
    seen_entries = set()

    while True:
        feed = feedparser.parse(url)
        current_time = datetime.utcnow()
        
        for entry in feed.entries:
            published = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
            
            if entry.link not in seen_entries and (current_time - published) < timedelta(hours=1):
                print(f"📡 {entry.title}")
                print(f"⏰ {published.strftime('%H:%M UTC')}")
                print(f"🔗 {entry.link}\n")
                seen_entries.add(entry.link)

track_rss('artificial+intelligence')
