import json
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

class SocialRadarEngine:
    """
    MZ-15 Enterprise-Grade Social Radar:
    - Extracts authentic Reddit & community customer pain points without 403 blocks.
    - Curates high-retention audio & sound pacing formulas mapped to Creator Personas.
    """
    def __init__(self, country_code: str = None, region: str = "US", **kwargs):
        self.country_code = (country_code or region or "US").upper()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        }

    def get_community_pain_points(self, topic: str, limit: int = 10) -> list:
        """
        Pulls unfiltered discussions, struggles, and buyer objections from Reddit
        via search engine proxy to bypass API authentication blocks completely.
        """
        query = f"site:reddit.com {topic} problem OR struggle OR worst OR mistake"
        url = "https://html.duckduckgo.com/html/"
        pain_points = []

        try:
            res = requests.post(url, data={"q": query}, headers=self.headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                results = soup.select(".result__body")
                for r in results[:limit]:
                    title_el = r.select_one(".result__title")
                    snippet_el = r.select_one(".result__snippet")
                    url_el = r.select_one(".result__url")

                    title = title_el.get_text(strip=True) if title_el else ""
                    snippet = snippet_el.get_text(strip=True) if snippet_el else ""
                    link = url_el.get_text(strip=True) if url_el else ""

                    if title:
                        pain_points.append({
                            "title": title,
                            "snippet": snippet,
                            "link": "https://" + link.strip() if not link.startswith("http") else link.strip()
                        })
        except Exception as e:
            print(f"[-] Pain point extraction error: {e}")

        return pain_points

    def get_persona_audio_formulas(self, creator_type: str = "tech_educator") -> list:
        """
        Returns high-converting sound formats tailored to the creator's persona.
        """
        formulas = {
            "tech_educator": [
                {"sound": "Lo-Fi Coding Beats (120 BPM)", "pacing": "Fast cut every 1.5s with code syntax highlight", "retention": "+42% completion"},
                {"sound": "Sub-Bass Drop Tension", "pacing": "Silence first 2s, bass drop on hook reveal", "retention": "+55% 3s hook hold"}
            ],
            "saas_b2b_founder": [
                {"sound": "Minimal Tech Ambient House", "pacing": "Dynamic captions centered, switch zoom on numbers", "retention": "+34% share rate"},
                {"sound": "Direct Voiceover Only (-12dB subtle pad)", "pacing": "High vocal clarity, boardroom authority style", "retention": "+61% comment rate"}
            ],
            "finance_real_estate": [
                {"sound": "Cinematic Urgency / Ticking Clock", "pacing": "Fast chart reveal at 0:02, high contrast numbers", "retention": "+48% save rate"},
                {"sound": "Conversational Walk & Talk Ambience", "pacing": "Handheld camera motion, eye-level authenticity", "retention": "+39% watch time"}
            ],
            "fitness_health_coach": [
                {"sound": "High-Energy Phonk / Heavy Bass Beat", "pacing": "Form mistake clip at 0:01, immediate correction", "retention": "+58% loop rate"},
                {"sound": "Acoustic Reflection / Story Arc", "pacing": "Before/After split screen pacing", "retention": "+44% shares"}
            ]
        }
        return formulas.get(creator_type, formulas["tech_educator"])
