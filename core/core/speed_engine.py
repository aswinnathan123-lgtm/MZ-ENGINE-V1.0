import requests

class SpeedAuditEngine:
    """
    Zero-key Performance & Core Web Vitals Engine.
    Leverages Google's free public PageSpeed Insights API endpoint to audit
    FCP, LCP, CLS, and Performance Scores without an API key.
    """
    def __init__(self):
        pass

    def run_speed_test(self, target_url: str, strategy: str = "mobile") -> dict:
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url

        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={target_url}&strategy={strategy}"

        try:
            res = requests.get(api_url, timeout=20)
            if res.status_code == 200:
                data = res.json()
                lighthouse = data.get("lighthouseResult", {})
                cats = lighthouse.get("categories", {})
                perf_score = int(cats.get("performance", {}).get("score", 0) * 100)

                audits = lighthouse.get("audits", {})
                fcp = audits.get("first-contentful-paint", {}).get("displayValue", "N/A")
                lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
                tbt = audits.get("total-blocking-time", {}).get("displayValue", "N/A")
                cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
                speed_index = audits.get("speed-index", {}).get("displayValue", "N/A")

                return {
                    "url": target_url,
                    "strategy": strategy,
                    "performance_score": perf_score,
                    "first_contentful_paint": fcp,
                    "largest_contentful_paint": lcp,
                    "total_blocking_time": tbt,
                    "cumulative_layout_shift": cls,
                    "speed_index": speed_index,
                    "grade": "GOOD (Fast)" if perf_score >= 80 else ("AVERAGE" if perf_score >= 50 else "POOR (Slow)")
                }
            else:
                return {"error": f"PageSpeed API returned status code {res.status_code}"}
        except Exception as e:
            return {"error": f"Speed audit request timed out or failed: {str(e)}"}
