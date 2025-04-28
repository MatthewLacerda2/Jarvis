import feedparser
from datetime import datetime, timedelta
from gnewsdecoder import decode

def track_rss(query):
    url = f"https://news.google.com/rss/search?q={query}+when:1h&ceid=US:en"

    feed = feedparser.parse(url)
    current_time = datetime.now()
    
    for entry in feed.entries:
        published = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
        
        if (current_time - published) < timedelta(hours=1):
            print(f"📡 {entry.title}")
            print(f"⏰ {published.strftime('%H:%M UTC')}")
            print(f"🔗 {entry.link}\n")
            
            decode(entry.link)

track_rss('artificial+intelligence')
