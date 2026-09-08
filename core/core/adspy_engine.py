from urllib.parse import quote_plus

class AdSpyEngine:
    """
    Zero-key Advertising & Paid Traffic Intelligence Engine.
    Generates direct queries to Meta Ad Library, Google Ads Transparency Center,
    and analyzes competitor creative patterns and hooks.
    """
    def __init__(self):
        pass

    def analyze_ads(self, brand_or_keyword: str) -> dict:
        q = brand_or_keyword.strip()
        q_enc = quote_plus(q)

        meta_library_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={q_enc}"
        google_transparency_url = f"https://adstransparency.google.com/?region=anywhere&query={q_enc}"
        tiktok_ad_url = f"https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en?keyword={q_enc}"

        ad_hooks = [
            {"hook_type": "Pain-Point Agitator", "angle": f"Tired of manual {q}? Here is what top teams do instead.", "format": "Short-form video UGC"},
            {"hook_type": "Social Proof / Numbers", "angle": f"Over 10,000+ businesses use this for {q} every day.", "format": "Carousel / Customer quote"},
            {"hook_type": "Contrarian Challenge", "angle": f"Stop doing {q} the old way. It is costing you time & profit.", "format": "Direct camera callout"},
            {"hook_type": "Direct Offer / Promotion", "angle": f"Limited time upgrade: Get 50% off {q} solutions today.", "format": "Static banner / Retargeting"}
        ]

        return {
            "target": q,
            "meta_ad_library_url": meta_library_url,
            "google_ad_transparency_url": google_transparency_url,
            "tiktok_creative_center_url": tiktok_ad_url,
            "suggested_ad_creative_angles": ad_hooks
        }
