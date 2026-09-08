import re
import json
from collections import Counter
import requests
from .constants import ELITE_6_HOOKS

class VideoForensicsEngine:
    """
    NASA-Grade YouTube Video Velocity & 6-Hook Radar.
    Detects which of the 6 Elite Hook Formats is trending right now in any Country/Locality.
    Calculates Views-Per-Hour (VPH) and format market share.
    """
    def __init__(self, country_code: str = None, region: str = "US", language: str = "en", **kwargs):
        self.country_code = (country_code or region or "US").upper()
        self.language = language.lower()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept-Language": f"{self.language}-{self.country_code},{self.language};q=0.9"
        }

    def _parse_relative_time_to_hours(self, text: str) -> float:
        if not text:
            return 24.0
        text = text.lower()
        match = re.search(r'(\d+)\s*(minute|hour|day|week|month|year)', text)
        if not match:
            return 24.0
        num = float(match.group(1))
        unit = match.group(2)
        if "minute" in unit:
            return max(0.1, num / 60.0)
        elif "hour" in unit:
            return max(1.0, num)
        elif "day" in unit:
            return num * 24.0
        elif "week" in unit:
            return num * 24.0 * 7.0
        elif "month" in unit:
            return num * 24.0 * 30.0
        elif "year" in unit:
            return num * 24.0 * 365.0
        return 24.0

    def _parse_view_count(self, view_str: str) -> int:
        if not view_str:
            return 0
        cleaned = view_str.lower().replace("views", "").replace("view", "").strip()
        try:
            if "k" in cleaned:
                return int(float(cleaned.replace("k", "").strip()) * 1000)
            elif "m" in cleaned:
                return int(float(cleaned.replace("m", "").strip()) * 1000000)
            elif "b" in cleaned:
                return int(float(cleaned.replace("b", "").strip()) * 1000000000)
            else:
                return int(re.sub(r'[^\d]', '', cleaned))
        except:
            return 0

    def classify_6_hook_archetype(self, title: str) -> dict:
        """
        Classifies video titles into the 6 Elite Hook Archetypes.
        """
        t = title.lower()
        detected_hooks = []

        # 1. The Fortune Teller (Future-pacing, change forever, prepare, new era)
        if any(k in t for k in ["change forever", "future of", "in 2026", "new era", "going to change", "prepare for", "will change", "is coming"]):
            detected_hooks.append("The Fortune Teller")

        # 2. The Contrarian (Stop doing, don't, actually hurting, lie about, mistake, dead)
        if any(k in t for k in ["stop ", "don't ", "dont ", "is dead", "waste of", "actually hurting", "mistake", "lie about", "ruining", "worst"]):
            detected_hooks.append("The Contrarian")

        # 3. The Insider (Nobody tells you, secret, hidden, truth about, exposed, what they won't)
        if any(k in t for k in ["nobody tells", "no one talks", "secret", "truth about", "exposed", "behind the scenes", "won't tell you", "what happens inside"]):
            detected_hooks.append("The Insider")

        # 4. The Proven Winner (Specific numbers, revenue, $, how I got X views/clients)
        if re.search(r'(\$\d+|₹\d+|\d+[km]\b|\d+\s*(leads|views|days|hours|clients|subscribers)|how\s+i\s+(made|got|scaled)|case\s+study)', t):
            detected_hooks.append("The Proven Winner")

        # 5. The Eye Magnet (Look at this, watch until, insane, mind-blowing, wait for it)
        if any(k in t for k in ["look at this", "watch until", "insane", "wait for it", "this happened", "mind-blowing", "unbelievable"]):
            detected_hooks.append("The Eye Magnet")

        # 6. The Connector (What does X have in common with Y, vs, meets, connection)
        if any(k in t for k in ["have in common", "what happens when", "meets", "compared to", " vs "]):
            detected_hooks.append("The Connector")

        primary_hook = detected_hooks[0] if detected_hooks else "Standard Explainer"
        return {
            "title": title,
            "primary_hook": primary_hook,
            "all_detected": detected_hooks or ["Standard Explainer"],
            "description": ELITE_6_HOOKS.get(primary_hook, {}).get("description", "Standard topic explainer")
        }

    def fetch_localized_youtube_radar(self, query: str, limit: int = 25) -> dict:
        """
        Extracts YouTube search results localized by country (gl) & language (hl).
        Computes VPH velocity and calculates the Hook Dominance Index.
        """
        search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}&gl={self.country_code}&hl={self.language}"
        videos = []

        try:
            res = requests.get(search_url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                html = res.text
                start_marker = "var ytInitialData = "
                start_idx = html.find(start_marker)
                
                if start_idx != -1:
                    raw_json = html[start_idx + len(start_marker): html.find(";</script>", start_idx)]
                    data = json.loads(raw_json)

                    contents = (
                        data.get("contents", {})
                        .get("twoColumnSearchResultsRenderer", {})
                        .get("primaryContents", {})
                        .get("sectionListRenderer", {})
                        .get("contents", [])
                    )

                    for sec in contents:
                        for item in sec.get("itemSectionRenderer", {}).get("contents", []):
                            v = item.get("videoRenderer")
                            if not v:
                                continue

                            video_id = v.get("videoId", "")
                            title = v.get("title", {}).get("runs", [{}])[0].get("text", "")
                            view_text = v.get("viewCountText", {}).get("simpleText", "") or v.get("viewCountText", {}).get("runs", [{}])[0].get("text", "")
                            published_text = v.get("publishedTimeText", {}).get("simpleText", "")
                            channel = v.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
                            
                            views = self._parse_view_count(view_text)
                            hours_ago = self._parse_relative_time_to_hours(published_text)
                            vph = round(views / max(1.0, hours_ago), 1)

                            hook_meta = self.classify_6_hook_archetype(title)

                            videos.append({
                                "video_id": video_id,
                                "url": f"https://www.youtube.com/watch?v={video_id}",
                                "title": title,
                                "channel": channel,
                                "views": views,
                                "views_formatted": view_text,
                                "published": published_text,
                                "vph": vph,
                                "hook": hook_meta["primary_hook"],
                                "hook_meta": hook_meta
                            })
                            if len(videos) >= limit:
                                break
                        if len(videos) >= limit:
                            break
        except Exception as e:
            print(f"[-] YouTube forensics error: {e}")

        # Calculate Hook Dominance Market Share
        hook_counts = Counter([v["hook"] for v in videos])
        total_vids = max(1, len(videos))
        hook_dominance = {}
        for h_name in list(ELITE_6_HOOKS.keys()) + ["Standard Explainer"]:
            count = hook_counts.get(h_name, 0)
            hook_dominance[h_name] = {
                "count": count,
                "percentage": round((count / total_vids) * 100, 1)
            }

        sorted_videos = sorted(videos, key=lambda x: x["vph"], reverse=True)
        return {
            "query": query,
            "country": self.country_code,
            "total_analyzed": len(videos),
            "hook_dominance": hook_dominance,
            "videos": sorted_videos,
            "top_breakout_video": sorted_videos[0] if sorted_videos else None,
            "average_vph": round(sum(v["vph"] for v in videos) / total_vids, 1)
        }
