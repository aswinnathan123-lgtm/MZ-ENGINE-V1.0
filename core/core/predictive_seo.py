import json
import string
from urllib.parse import quote_plus
import requests

class PredictiveSEOEngine:
    """
    MZ-15 Enterprise-Grade Localized Predictive SEO & Search Demand Matrix.
    Supports Worldwide Geo-Targeting (gl/hl), Postal/Pincode Hyper-Local Expansion,
    and Creator Persona Intent Classification. Zero API keys.
    """
    def __init__(self, country_code: str = None, region: str = "US", language: str = "en", pincode: str = "", **kwargs):
        self.country_code = (country_code or region or "US").upper()
        self.region = self.country_code
        self.language = language.lower()
        self.pincode = pincode.strip() if pincode else ""
        self.session = requests.Session()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept-Language": f"{self.language}-{self.country_code},{self.language};q=0.9"
        }

    def _query_autocomplete(self, query: str, platform: str = "google") -> list:
        """Fetch raw real-time search queries from Google or YouTube with geo-targeting."""
        ds_param = "yt" if platform == "youtube" else ""
        url = (
            f"https://suggestqueries.google.com/complete/search?"
            f"client=firefox&ds={ds_param}&hl={self.language}&gl={self.country_code}&q={quote_plus(query)}"
        )
        try:
            res = self.session.get(url, headers=self.headers, timeout=4)
            if res.status_code == 200:
                data = res.json()
                if len(data) > 1 and isinstance(data[1], list):
                    return data[1]
        except Exception:
            pass
        return []

    def run_deep_matrix(self, seed: str, platform: str = "google", max_alpha: int = 12) -> dict:
        """
        Executes a 360-degree intent matrix localized to Country and Pincode:
        - Core seed suggestions
        - Hyper-local / Pincode intent variants
        - 7W1H Question Taxonomy
        - Commercial & Buyer Intent
        - Alphabet Soup (A-Z)
        """
        clean_seed = seed.strip().lower()
        matrix = {
            "seed": clean_seed,
            "country": self.country_code,
            "pincode": self.pincode,
            "platform": platform,
            "core_intent": [],
            "pincode_localized_queries": [],
            "questions": {
                "how": [],
                "what": [],
                "why": [],
                "who": [],
                "where": [],
                "when": [],
                "can_or_will": [],
                "best_or_which": []
            },
            "commercial": [],
            "alphabet_soup": {},
            "all_unique_queries": []
        }

        all_discovered = set()

        # 1. Base query
        base_queries = self._query_autocomplete(clean_seed, platform)
        matrix["core_intent"] = base_queries
        all_discovered.update(base_queries)

        # 2. Hyper-Local & Pincode Expansions (if pincode is provided)
        if self.pincode:
            local_patterns = [
                f"{clean_seed} in {self.pincode}",
                f"{clean_seed} near {self.pincode}",
                f"best {clean_seed} {self.pincode}",
                f"{clean_seed} service {self.pincode}"
            ]
            for pat in local_patterns:
                l_res = self._query_autocomplete(pat, platform)
                matrix["pincode_localized_queries"].extend(l_res)
                all_discovered.update(l_res)
            matrix["pincode_localized_queries"] = list(dict.fromkeys(matrix["pincode_localized_queries"]))

        # 3. 7W1H Questions
        question_patterns = {
            "how": [f"how to {clean_seed}", f"how does {clean_seed}"],
            "what": [f"what is {clean_seed}", f"what does {clean_seed}"],
            "why": [f"why {clean_seed}", f"why use {clean_seed}"],
            "who": [f"who uses {clean_seed}", f"who makes {clean_seed}"],
            "where": [f"where to buy {clean_seed}", f"where to find {clean_seed}"],
            "when": [f"when to use {clean_seed}"],
            "can_or_will": [f"can {clean_seed}", f"will {clean_seed}"],
            "best_or_which": [f"which {clean_seed}", f"best {clean_seed} for"]
        }

        for category, patterns in question_patterns.items():
            cat_results = []
            for pat in patterns:
                results = self._query_autocomplete(pat, platform)
                cat_results.extend(results)
                all_discovered.update(results)
            matrix["questions"][category] = list(dict.fromkeys(cat_results))

        # 4. Commercial Intent
        comm_modifiers = ["price", "cost", "review", "vs", "alternative to", "cheap", "buy", "service"]
        for mod in comm_modifiers:
            queries = self._query_autocomplete(f"{clean_seed} {mod}", platform)
            matrix["commercial"].extend(queries)
            all_discovered.update(queries)
        matrix["commercial"] = list(dict.fromkeys(matrix["commercial"]))

        # 5. Alphabet Soup
        letters = list(string.ascii_lowercase)[:max_alpha]
        for letter in letters:
            queries = self._query_autocomplete(f"{clean_seed} {letter}", platform)
            if queries:
                matrix["alphabet_soup"][letter] = queries
                all_discovered.update(queries)

        matrix["all_unique_queries"] = sorted(list(all_discovered))
        matrix["total_queries_found"] = len(matrix["all_unique_queries"])
        return matrix
