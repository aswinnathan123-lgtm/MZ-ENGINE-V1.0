import hashlib
import requests

class BreachRadarEngine:
    """
    Zero-key Credential Leak & Security Exposure Engine.
    Uses NIST-compliant k-Anonymity (Pwned Passwords API) to check password breaches without revealing user data,
    and queries public breach directories.
    """
    def __init__(self):
        self.headers = {"User-Agent": "NASA-BreachRadar-OSINT/3.4"}

    def check_password_exposure(self, password: str) -> dict:
        """
        Computes SHA-1 hash, sends only the first 5 characters (k-Anonymity),
        and verifies if the remaining hash matches any known breach record.
        """
        if not password:
            return {"error": "Password input is empty."}
        
        sha1_pwd = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix = sha1_pwd[:5]
        suffix = sha1_pwd[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            res = requests.get(url, headers=self.headers, timeout=6)
            if res.status_code == 200:
                hashes = (line.split(":") for line in res.text.splitlines())
                for h_suffix, count in hashes:
                    if h_suffix.upper() == suffix:
                        times_seen = int(count)
                        return {
                            "compromised": True,
                            "times_seen": times_seen,
                            "risk_level": "CRITICAL" if times_seen > 1000 else "HIGH",
                            "verdict": f"🚨 COMPROMISED! Leaked in {times_seen:,} data breaches."
                        }
                return {
                    "compromised": False,
                    "times_seen": 0,
                    "risk_level": "SAFE",
                    "verdict": "🟢 CLEAN! Not found in public credential dumps."
                }
        except Exception as e:
            return {"error": f"Breach check connection failed: {str(e)}"}
        
        return {"error": "Unexpected API response."}
