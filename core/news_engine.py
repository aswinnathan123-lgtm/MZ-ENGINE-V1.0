import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
import requests

class NewsPulseEngine:
    """
    Omni-News Intelligence Engine.
    Covers everything: Global Breaking, India National, Tech & AI, Financial Markets,
    Defense & Military, Science & Space, and custom search queries with live sentiment.
    """
    TOPICS = {
        "WORLD": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "NATION": "https://news.google.com/rss/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE?hl={lang}&gl={country}&ceid={country}:{lang}",
        "BUSINESS": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "TECHNOLOGY": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "SCIENCE": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "ENTERTAINMENT": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}"
    }

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_news(self, query: str = "", category: str = "ALL", country: str = "US", language: str = "en", limit: int = 15) -> dict:
        country = country.upper()
        lang = language.lower()

        if category.upper() in self.TOPICS and not query:
            url = self.TOPICS[category.upper()].format(country=country, lang=lang)
        elif query:
            q_enc = quote_plus(query.strip())
            url = f"https://news.google.com/rss/search?q={q_enc}&hl={lang}&gl={country}&ceid={country}:{lang}"
        else:
            url = self.TOPICS["WORLD"].format(country=country, lang=lang)

        articles = []
        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                channel = root.find("channel")
                if channel:
                    for item in channel.findall("item")[:limit]:
                        title = item.find("title").text if item.find("title") is not None else ""
                        link = item.find("link").text if item.find("link") is not None else ""
                        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                        source = item.find("source").text if item.find("source") is not None else "Google News"

                        t_lower = title.lower()
                        if any(w in t_lower for w in ["surge", "record", "growth", "boom", "rally", "breakthrough", "profit", "win", "bull"]):
                            sentiment = "BULLISH / POSITIVE"
                        elif any(w in t_lower for w in ["crash", "drop", "plunge", "ban", "loss", "layoff", "sue", "scandal", "crisis", "war"]):
                            sentiment = "BEARISH / NEGATIVE"
                        else:
                            sentiment = "NEUTRAL"

                        articles.append({
                            "title": title,
                            "link": link,
                            "pub_date": pub_date,
                            "source": source,
                            "sentiment": sentiment
                        })
        except Exception as e:
            return {"query": query or category, "error": str(e), "articles": []}

        return {
            "query": query or category,
            "category": category,
            "country": country,
            "total_articles": len(articles),
            "articles": articles
        }
