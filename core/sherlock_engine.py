import concurrent.futures
import requests

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter / X": "https://x.com/{}",
    "Reddit": "https://www.reddit.com/user/{}/",
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Medium": "https://medium.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Telegram": "https://t.me/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "GitLab": "https://gitlab.com/{}",
    "Keybase": "https://keybase.io/{}",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Substack": "https://{}.substack.com",
    "DeviantArt": "https://www.deviantart.com/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Vimeo": "https://vimeo.com/{}"
}

class SherlockSocialEngine:
    """
    Fast, concurrent username reconnaissance engine across 24+ top platforms.
    100% authentic HTTP status checks without API keys.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

    def _check_platform(self, name: str, url_tpl: str, username: str) -> dict:
        target_url = url_tpl.format(username)
        try:
            res = requests.get(target_url, headers=self.headers, timeout=4, allow_redirects=True)
            exists = res.status_code == 200
            return {
                "platform": name,
                "url": target_url,
                "status_code": res.status_code,
                "exists": exists
            }
        except Exception:
            return {
                "platform": name,
                "url": target_url,
                "status_code": 0,
                "exists": False
            }

    def scan_username(self, username: str, max_workers: int = 15) -> dict:
        username = username.strip().lstrip("@")
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_platform = {
                executor.submit(self._check_platform, name, url_tpl, username): name
                for name, url_tpl in PLATFORMS.items()
            }
            for future in concurrent.futures.as_completed(future_to_platform):
                results.append(future.result())

        found = [r for r in results if r["exists"]]
        missing = [r for r in results if not r["exists"]]

        return {
            "username": username,
            "total_scanned": len(PLATFORMS),
            "found_count": len(found),
            "presence_rate": round((len(found) / len(PLATFORMS)) * 100, 1),
            "found_profiles": sorted(found, key=lambda x: x["platform"]),
            "missing_profiles": sorted(missing, key=lambda x: x["platform"])
        }
