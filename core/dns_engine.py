import socket
from urllib.parse import urlparse
import requests

class DNSMasterEngine:
    """
    Zero-key DNS, WHOIS & IP Geolocation Reconnaissance Engine.
    Uses public DNS-over-HTTPS (Cloudflare / Google) and IP Geolocation endpoints.
    """
    def __init__(self):
        self.headers = {"Accept": "application/dns-json"}

    def clean_domain(self, target: str) -> str:
        clean = target.strip().lower()
        if clean.startswith("http://") or clean.startswith("https://"):
            clean = urlparse(clean).netloc
        if clean.startswith("www."):
            clean = clean[4:]
        return clean.split("/")[0].split(":")[0]

    def _query_doh(self, domain: str, record_type: str) -> list:
        url = f"https://cloudflare-dns.com/dns-query?name={domain}&type={record_type}"
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                answers = data.get("Answer", [])
                return [a.get("data") for a in answers if a.get("data")]
        except Exception:
            pass
        return []

    def get_dns_and_ip_dossier(self, target: str) -> dict:
        domain = self.clean_domain(target)
        records = {
            "A": self._query_doh(domain, "A"),
            "AAAA": self._query_doh(domain, "AAAA"),
            "MX": self._query_doh(domain, "MX"),
            "NS": self._query_doh(domain, "NS"),
            "TXT": self._query_doh(domain, "TXT"),
            "SOA": self._query_doh(domain, "SOA")
        }

        # Resolve primary IP
        primary_ip = records["A"][0] if records["A"] else None
        geo_info = {}
        if primary_ip:
            try:
                g_res = requests.get(f"http://ip-api.com/json/{primary_ip}", timeout=5)
                if g_res.status_code == 200:
                    geo_info = g_res.json()
            except Exception:
                pass

        return {
            "domain": domain,
            "primary_ip": primary_ip or "Unresolved",
            "records": records,
            "geo": {
                "country": geo_info.get("country", "Unknown"),
                "country_code": geo_info.get("countryCode", "N/A"),
                "region_name": geo_info.get("regionName", "Unknown"),
                "city": geo_info.get("city", "Unknown"),
                "isp": geo_info.get("isp", "Unknown"),
                "org": geo_info.get("org", "Unknown"),
                "asn": geo_info.get("as", "Unknown"),
                "timezone": geo_info.get("timezone", "UTC")
            }
        }
