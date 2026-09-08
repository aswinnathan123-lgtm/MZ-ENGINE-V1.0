import re
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

class BrandForensicsEngine:
    """
    Zero-key Brand & Visual Asset Reconnaissance.
    Extracts brand logos, high-res favicons, OpenGraph images, social footprints, and color codes.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

    def clean_url(self, target: str) -> str:
        clean = target.strip()
        if not clean.startswith("http://") and not clean.startswith("https://"):
            clean = "https://" + clean
        return clean

    def extract_brand_assets(self, target: str) -> dict:
        url = self.clean_url(target)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        assets = {
            "domain": parsed.netloc,
            "favicon": "",
            "apple_icon": "",
            "og_image": "",
            "logo_images": [],
            "brand_colors": [],
            "social_links": []
        }

        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")

                # Favicons
                icon = soup.find("link", rel=lambda x: x and ("icon" in x.lower() or "shortcut icon" in x.lower()))
                if icon and icon.get("href"):
                    assets["favicon"] = urljoin(base, icon.get("href"))
                else:
                    assets["favicon"] = f"{base}/favicon.ico"

                apple = soup.find("link", rel=lambda x: x and "apple-touch-icon" in x.lower())
                if apple and apple.get("href"):
                    assets["apple_icon"] = urljoin(base, apple.get("href"))

                # OpenGraph
                og = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
                if og and og.get("content"):
                    assets["og_image"] = urljoin(base, og.get("content"))

                # Logos in img tags
                logos = []
                for img in soup.find_all("img"):
                    src = img.get("src", "")
                    alt = img.get("alt", "").lower()
                    cls = " ".join(img.get("class", [])).lower()
                    if "logo" in src.lower() or "logo" in alt or "logo" in cls:
                        logos.append(urljoin(base, src))
                assets["logo_images"] = list(set(logos))[:5]

                # Hex colors from inline styles or style tags
                hex_colors = set(re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}', res.text))
                # Filter out pure black and pure white
                clean_colors = [c.upper() for c in hex_colors if c.upper() not in ["#000", "#000000", "#FFF", "#FFFFFF"]][:6]
                assets["brand_colors"] = clean_colors

                # Social links
                social_domains = ["twitter.com", "x.com", "linkedin.com", "github.com", "facebook.com", "instagram.com", "youtube.com", "discord.gg"]
                s_links = set()
                for a in soup.find_all("a", href=True):
                    h = a["href"]
                    if any(sd in h for sd in social_domains):
                        s_links.add(h)
                assets["social_links"] = list(s_links)[:8]

        except Exception as e:
            assets["error"] = str(e)

        return assets
