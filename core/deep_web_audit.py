import json
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class DeepWebAuditor:
    """
    NASA-Grade Competitor Reverse Engineering:
    - Zero-key replacement for SecurityTrails (crt.sh Certificate Transparency).
    - Zero-key replacement for BuiltWith (HTTP Headers & DOM signatures).
    - On-page technical SEO & Schema audit.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        }

    def clean_domain(self, target: str) -> str:
        target = target.strip().lower()
        if not target.startswith("http://") and not target.startswith("https://"):
            target = "https://" + target
        parsed = urlparse(target)
        netloc = parsed.netloc or parsed.path
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc.split("/")[0].split(":")[0]

    def get_subdomains_via_cert_transparency(self, domain: str, max_limit: int = 50) -> dict:
        clean_dom = self.clean_domain(domain)
        url = f"https://crt.sh/?q=%.{clean_dom}&output=json"
        subdomains = set()

        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                for entry in data:
                    name_value = entry.get("name_value", "")
                    for sub in name_value.split("\n"):
                        sub = sub.strip().lower()
                        if sub.startswith("*."):
                            sub = sub[2:]
                        if sub.endswith(clean_dom) and len(sub) > len(clean_dom):
                            subdomains.add(sub)
                
                classified = []
                interest_regex = re.compile(r'(admin|api|v[0-9]|staging|dev|internal|vpn|auth|portal|test)', re.I)
                for s in sorted(list(subdomains))[:max_limit]:
                    classified.append({
                        "subdomain": s,
                        "type": "High-Value Staging/Internal" if interest_regex.search(s) else "Standard Production"
                    })

                return {
                    "domain": clean_dom,
                    "total_found": len(subdomains),
                    "subdomains": classified
                }
        except Exception as e:
            return {"domain": clean_dom, "error": str(e), "subdomains": []}

        return {"domain": clean_dom, "total_found": 0, "subdomains": []}

    def fingerprint_tech_stack(self, url: str) -> dict:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        tech = {
            "server": "Unknown",
            "frameworks": [],
            "cms": [],
            "analytics_and_ads": [],
            "cdn_or_waf": []
        }

        try:
            res = requests.get(url, headers=self.headers, timeout=6)
            headers = res.headers
            body = res.text.lower()

            if "server" in headers:
                tech["server"] = headers["server"]
            if "cf-ray" in headers or "cloudflare" in headers.get("server", "").lower():
                tech["cdn_or_waf"].append("Cloudflare")
            if "x-amz-cf-id" in headers or "cloudfront" in headers.get("via", "").lower():
                tech["cdn_or_waf"].append("AWS CloudFront")

            if "__next" in body:
                tech["frameworks"].append("Next.js")
            elif "react" in body:
                tech["frameworks"].append("React")
            if "/wp-content/" in body:
                tech["cms"].append("WordPress")
            if "shopify" in body:
                tech["cms"].append("Shopify")
            if "googletagmanager" in body:
                tech["analytics_and_ads"].append("Google Tag Manager")
            if "fbq(" in body:
                tech["analytics_and_ads"].append("Meta Pixel")

            tech["frameworks"] = list(set(tech["frameworks"]))
            tech["cms"] = list(set(tech["cms"]))
            tech["analytics_and_ads"] = list(set(tech["analytics_and_ads"]))
            tech["cdn_or_waf"] = list(set(tech["cdn_or_waf"]))
        except Exception as e:
            tech["error"] = str(e)

        return tech

    def audit_onpage_seo(self, url: str) -> dict:
        """Complete on-page technical SEO & Schema health audit."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        result = {
            "url": url,
            "title": "",
            "title_length": 0,
            "title_status": "Missing",
            "description": "",
            "description_length": 0,
            "description_status": "Missing",
            "h1_count": 0,
            "h1_elements": [],
            "h2_count": 0,
            "h2_elements": [],
            "word_count": 0,
            "canonical": "",
            "schemas_detected": [],
            "og_title": "",
            "og_image": "",
            "robots_txt_found": False,
            "sitemap_xml_found": False,
            "seo_grade": "B"
        }

        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            soup = BeautifulSoup(res.text, "html.parser")

            # Title
            if soup.title and soup.title.string:
                result["title"] = soup.title.string.strip()
                result["title_length"] = len(result["title"])
                result["title_status"] = "Optimal (50-60 chars)" if 40 <= result["title_length"] <= 65 else "Warning (Length)"

            # Meta Description
            meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
            if meta_desc and meta_desc.get("content"):
                result["description"] = meta_desc["content"].strip()
                result["description_length"] = len(result["description"])
                result["description_status"] = "Optimal (120-160 chars)" if 110 <= result["description_length"] <= 165 else "Warning (Length)"

            # Headings
            h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
            result["h1_count"] = len(h1s)
            result["h1_elements"] = h1s[:5]
            h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
            result["h2_count"] = len(h2s)
            result["h2_elements"] = h2s[:8]

            # Word count
            text = soup.get_text()
            words = [w for w in text.split() if len(w) > 1]
            result["word_count"] = len(words)

            # Canonical
            can = soup.find("link", rel="canonical")
            if can and can.get("href"):
                result["canonical"] = can.get("href")

            # OpenGraph
            og_t = soup.find("meta", property="og:title")
            if og_t: result["og_title"] = og_t.get("content", "")
            og_i = soup.find("meta", property="og:image")
            if og_i: result["og_image"] = og_i.get("content", "")

            # Schemas
            for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
                try:
                    if s.string:
                        sd = json.loads(s.string)
                        if isinstance(sd, dict):
                            result["schemas_detected"].append(sd.get("@type", "Schema"))
                        elif isinstance(sd, list):
                            for item in sd:
                                if isinstance(item, dict):
                                    result["schemas_detected"].append(item.get("@type", "Schema"))
                except: pass
            result["schemas_detected"] = list(set(result["schemas_detected"]))

            # Sitemaps & robots.txt check
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            try:
                r_rob = requests.get(f"{base_url}/robots.txt", headers=self.headers, timeout=3)
                result["robots_txt_found"] = (r_rob.status_code == 200)
            except: pass
            try:
                r_sm = requests.get(f"{base_url}/sitemap.xml", headers=self.headers, timeout=3)
                result["sitemap_xml_found"] = (r_sm.status_code == 200)
            except: pass

            # Calculate Grade
            score = 100
            if not result["title"]: score -= 25
            if not result["description"]: score -= 20
            if result["h1_count"] == 0 or result["h1_count"] > 1: score -= 15
            if result["word_count"] < 300: score -= 15
            if not result["schemas_detected"]: score -= 10
            if not result["robots_txt_found"]: score -= 5
            if not result["sitemap_xml_found"]: score -= 10

            if score >= 85: result["seo_grade"] = "A (Excellent)"
            elif score >= 70: result["seo_grade"] = "B (Good)"
            elif score >= 50: result["seo_grade"] = "C (Needs Work)"
            else: result["seo_grade"] = "F (Poor)"

        except Exception as e:
            result["error"] = str(e)

        return result

    def check_serp_rank(self, domain: str, keyword: str) -> dict:
        """Extracts server-rendered organic positions for a domain without API keys."""
        clean_dom = self.clean_domain(domain)
        url = "https://html.duckduckgo.com/html/"
        position = "Not in Top 30"
        competitors = []

        try:
            r = requests.post(url, data={"q": keyword}, headers=self.headers, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                results = soup.select(".result__body")
                for idx, res in enumerate(results, 1):
                    url_elem = res.select_one(".result__url")
                    title_elem = res.select_one(".result__title")
                    
                    if url_elem:
                        url_text = url_elem.get_text(strip=True).lower()
                        title_text = title_elem.get_text(strip=True) if title_elem else "Result"
                        competitors.append({"rank": idx, "title": title_text[:50], "url": url_text[:45]})
                        
                        if clean_dom in url_text and position == "Not in Top 30":
                            position = f"#{idx}"
        except Exception:
            pass

        return {
            "domain": clean_dom,
            "keyword": keyword,
            "rank": position,
            "competitors": competitors[:5]
        }
