from urllib.parse import quote_plus
import requests

class PodcastRadarEngine:
    """
    Zero-key Audio & Podcast Research Engine.
    Queries Apple Podcasts public search API to discover trending shows, episode counts,
    creators, artwork, and RSS feed channels.
    """
    def __init__(self):
        self.headers = {"User-Agent": "NASA-PodcastRadar/3.4"}

    def search_podcasts(self, query: str, limit: int = 12) -> dict:
        q_enc = quote_plus(query.strip())
        url = f"https://itunes.apple.com/search?term={q_enc}&media=podcast&limit={limit}"

        podcasts = []
        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                for item in data.get("results", []):
                    podcasts.append({
                        "name": item.get("collectionName", "Unknown"),
                        "artist": item.get("artistName", "Unknown"),
                        "episodes": item.get("trackCount", 0),
                        "primary_genre": item.get("primaryGenreName", "Podcast"),
                        "feed_url": item.get("feedUrl", ""),
                        "artwork": item.get("artworkUrl600") or item.get("artworkUrl100", ""),
                        "itunes_url": item.get("collectionViewUrl", "")
                    })
        except Exception as e:
            return {"query": query, "error": str(e), "podcasts": []}

        return {
            "query": query,
            "total_found": len(podcasts),
            "podcasts": podcasts
        }
