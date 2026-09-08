import re
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
import requests

class NewsPulseEngine:
    """
    Zero-key Omni-News Intelligence & Viral Media Radar Engine.
    Covers 14+ deep categories: Global Breaking, India National, Tech, AI & Silicon,
    Business & Financial Markets, Defense & Geopolitics, Science & Space, Health,
    Clean Energy, Sports, Entertainment, Crypto, and Startups.
    Includes automated Inshorts-style 60-word micro-summaries, virality & share scoring,
    sentiment forensics, and native client sponsored ad generation.
    """

    TOPICS = {
        "WORLD": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "NATION": "https://news.google.com/rss/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE?hl={lang}&gl={country}&ceid={country}:{lang}",
        "BUSINESS": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "TECHNOLOGY": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "SCIENCE": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "HEALTH": "https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "SPORTS": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}",
        "ENTERTAINMENT": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl={lang}&gl={country}&ceid={country}:{lang}"
    }

    SPECIALIZED_QUERIES = {
        "AI": "Artificial Intelligence OR OpenAI OR Nvidia OR Anthropic OR LLM OR Gemini OR DeepSeek",
        "DEFENSE": "Defense military missiles NATO Indo-Pacific army warhead weapons",
        "ENERGY": "Renewable energy solar EV battery electric vehicles green hydrogen climate",
        "CRYPTO": "Bitcoin Ethereum crypto SEC ETF blockchain altcoins",
        "STARTUPS": "Startups venture capital funding seed round IPO unicorn Y Combinator",
        "POLICY": "Supreme Court regulation antitrust privacy government policy legislation"
    }

    TIER_ONE_SOURCES = [
        "reuters", "bloomberg", "the hindu", "times of india", "financial times",
        "wall street journal", "cnbc", "bbc", "techcrunch", "the verge",
        "economic times", "livemint", "ndtv", "indian express", "moneycontrol"
    ]

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        }

    def _strip_html(self, raw_html: str) -> str:
        """Removes HTML tags and cleans up entity codes."""
        if not raw_html:
            return ""
        clean = re.sub(r"<[^>]+>", " ", raw_html)
        clean = clean.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")
        return re.sub(r"\s+", " ", clean).strip()

    def _determine_tag(self, title: str, category: str) -> str:
        """Assigns high-granularity micro-topic tags."""
        t_low = title.lower()
        if any(w in t_low for w in ["ai", "llm", "gpt", "nvidia", "deep learning", "robotics", "gemini", "claude"]):
            return "🤖 AI & Silicon"
        elif any(w in t_low for w in ["market", "sensex", "nifty", "nasdaq", "stock", "shares", "fed", "inflation", "rbi"]):
            return "📈 Markets & Finance"
        elif any(w in t_low for w in ["isro", "nasa", "space", "moon", "satellite", "mars", "galaxy"]):
            return "🚀 Space & Science"
        elif any(w in t_low for w in ["defense", "army", "navy", "missile", "war", "security", "border", "pentagon"]):
            return "🛡️ Defense & Geopolitics"
        elif any(w in t_low for w in ["ev", "electric vehicle", "solar", "battery", "tesla", "climate", "green"]):
            return "⚡ CleanTech & EVs"
        elif any(w in t_low for w in ["funding", "valuation", "startup", "unicorn", "seed", "acquisition", "ipo"]):
            return "🦄 Startups & Deals"
        elif any(w in t_low for w in ["crypto", "bitcoin", "ethereum", "blockchain", "solana"]):
            return "🪙 Crypto & Web3"
        elif any(w in t_low for w in ["court", "law", "supreme court", "antitrust", "ban", "arrest", "police"]):
            return "⚖️ Legal & Policy"
        elif any(w in t_low for w in ["cricket", "bcci", "ipl", "football", "goal", "fifa", "olympic"]):
            return "🏏 Sports Arena"
        elif any(w in t_low for w in ["movie", "cinema", "box office", "actor", "hollywood", "bollywood", "netflix", "trailer"]):
            return "🎬 Pop Culture & Cinema"
        elif any(w in t_low for w in ["health", "vaccine", "cancer", "fda", "hospital", "pharma", "clinical"]):
            return "🏥 Healthcare & Bio"
        elif any(w in t_low for w in ["india", "delhi", "mumbai", "bengaluru", "chennai", "modi", "parliament"]):
            return "🇮🇳 India Spotlight"
        else:
            return f"🌍 {category.title()}"

    def _compute_virality(self, title: str, source: str, index: int) -> dict:
        """
        Calculates social virality and shareability metrics.
        Higher scores for breaking events, numbers, power verbs, and Tier-1 publishers.
        """
        t_low = title.lower()
        score = 65

        # Power keywords trigger virality
        power_triggers = [
            "breaking", "historic", "record", "surge", "plunge", "crisis", "shocking",
            "unveils", "banned", "leak", "secret", "trillion", "billion", "exclusive",
            "warning", "alert", "massive", "investigation", "explosion", "scandal"
        ]
        hits = sum(1 for w in power_triggers if w in t_low)
        score += min(22, hits * 6)

        # Source credibility boost
        if any(s in source.lower() for s in self.TIER_ONE_SOURCES):
            score += 7

        # Top articles in RSS have higher freshness velocity
        if index < 3:
            score += 5
        elif index < 7:
            score += 3

        # Cap score between 68 and 99
        final_score = min(99, max(68, score))

        if final_score >= 90:
            badge = "🔥 ULTRA VIRAL"
            color = "#ef4444"
            est_shares = f"{round(45.0 + (final_score - 90) * 8.5, 1)}K Shares"
        elif final_score >= 80:
            badge = "⚡ FAST SPREADING"
            color = "#f59e0b"
            est_shares = f"{round(18.0 + (final_score - 80) * 2.7, 1)}K Shares"
        elif final_score >= 72:
            badge = "📈 HIGH RESONANCE"
            color = "#3b82f6"
            est_shares = f"{round(8.5 + (final_score - 72) * 1.2, 1)}K Shares"
        else:
            badge = "📌 TRENDING"
            color = "#10b981"
            est_shares = f"{round(3.5 + final_score * 0.05, 1)}K Shares"

        return {
            "score": final_score,
            "badge": badge,
            "color": color,
            "est_shares": est_shares
        }

    def _generate_inshorts_summary(self, title: str, raw_snippet: str, source: str, tag: str) -> dict:
        """
        Synthesizes a punchy, clean 60-word Inshorts-style executive briefing
        plus 3 core takeaways and reading speed.
        """
        clean_snippet = self._strip_html(raw_snippet)

        # Extract core sentence from snippet or fall back to title context
        meaningful_snippet = ""
        if clean_snippet and len(clean_snippet) > 40:
            # Often Google News snippets have source attribution at the end
            parts = clean_snippet.split(" - ")
            meaningful_snippet = parts[0].strip()

        # Build punchy 60-word short briefing
        if meaningful_snippet and meaningful_snippet.lower() not in title.lower():
            body = f"{title.rstrip('.')}. {meaningful_snippet.rstrip('.')}."
        else:
            body = (
                f"{title.rstrip('.')}. Industry analysts and field observers note this marks a key milestone "
                f"across {tag.replace('🤖 ', '').replace('📈 ', '').replace('🚀 ', '')} ecosystems, signaling shifted "
                f"momentum and heightened public attention."
            )

        # Truncate to ~55-65 words
        words = body.split()
        if len(words) > 65:
            body_60 = " ".join(words[:62]) + "..."
        else:
            body_60 = " ".join(words)

        # 3 Structured Takeaways
        takeaways = [
            f"Key Event: {title[:75]}...",
            f"Strategic Impact: Amplifies momentum across {tag} sectors globally.",
            f"What to Watch: Regulatory and market reaction following publication by {source}."
        ]

        return {
            "short_text": body_60,
            "takeaways": takeaways,
            "word_count": len(body_60.split()),
            "read_time": "30 sec read"
        }

    def fetch_news(self, query: str = "", category: str = "ALL", country: str = "IN", language: str = "en", limit: int = 25) -> dict:
        """
        Fetches news articles with sentiment, Inshorts-style summaries,
        and shareability rankings across standard and specialized categories.
        """
        country = country.upper()
        lang = language.lower()
        cat_upper = category.upper()

        # Resolve RSS endpoint
        if query:
            q_enc = quote_plus(query.strip())
            url = f"https://news.google.com/rss/search?q={q_enc}&hl={lang}&gl={country}&ceid={country}:{lang}"
            stream_label = f"Search: '{query}'"
        elif cat_upper in self.SPECIALIZED_QUERIES:
            q_enc = quote_plus(self.SPECIALIZED_QUERIES[cat_upper])
            url = f"https://news.google.com/rss/search?q={q_enc}&hl={lang}&gl={country}&ceid={country}:{lang}"
            stream_label = f"Specialized: {category}"
        elif cat_upper in self.TOPICS:
            url = self.TOPICS[cat_upper].format(country=country, lang=lang)
            stream_label = f"Category: {category}"
        else:
            url = self.TOPICS["WORLD"].format(country=country, lang=lang)
            stream_label = "Global Breaking News"

        articles = []
        try:
            res = requests.get(url, headers=self.headers, timeout=9)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                channel = root.find("channel")
                if channel:
                    items = channel.findall("item")
                    for idx, item in enumerate(items[:limit]):
                        raw_title = item.findtext("title", "").strip()
                        link = item.findtext("link", "").strip()
                        pub_date = item.findtext("pubDate", "").strip()
                        desc_raw = item.findtext("description", "")
                        source_elem = item.find("source")
                        source = source_elem.text.strip() if source_elem is not None and source_elem.text else ""

                        # Separate headline and source if concatenated
                        title = raw_title
                        if not source and " - " in raw_title:
                            parts = raw_title.rsplit(" - ", 1)
                            title = parts[0].strip()
                            source = parts[1].strip()

                        if not source:
                            source = "Verified Wire"

                        # Clean date
                        display_date = pub_date[:16] if pub_date else "Recent"

                        # Sentiment analysis
                        t_lower = title.lower()
                        if any(w in t_lower for w in ["surge", "record", "growth", "boom", "rally", "breakthrough", "profit", "win", "bull", "triumph", "expansion"]):
                            sentiment = "BULLISH / POSITIVE"
                        elif any(w in t_lower for w in ["crash", "drop", "plunge", "ban", "loss", "layoff", "sue", "scandal", "crisis", "war", "death", "fraud"]):
                            sentiment = "BEARISH / NEGATIVE"
                        elif any(w in t_lower for w in ["investigation", "probe", "alert", "curb", "scrutiny", "arrest", "conflict"]):
                            sentiment = "SENSITIVE / WATCH"
                        else:
                            sentiment = "NEUTRAL / FACTUAL"

                        # Micro tag & Virality
                        tag = self._determine_tag(title, category)
                        virality = self._compute_virality(title, source, idx)

                        # 60-Word Inshorts Briefing
                        inshorts = self._generate_inshorts_summary(title, desc_raw, source, tag)

                        # Social share texts
                        encoded_title = quote_plus(f"{title} - Read on OmniNews: {link}")
                        whatsapp_link = f"https://api.whatsapp.com/send?text={encoded_title}"
                        linkedin_link = f"https://www.linkedin.com/sharing/share-offsite/?url={quote_plus(link)}"
                        x_link = f"https://twitter.com/intent/tweet?text={encoded_title}"

                        articles.append({
                            "id": f"news_{idx+1}",
                            "title": title,
                            "link": link,
                            "pub_date": display_date,
                            "source": source,
                            "sentiment": sentiment,
                            "tag": tag,
                            "virality": virality,
                            "inshorts": inshorts,
                            "whatsapp_link": whatsapp_link,
                            "linkedin_link": linkedin_link,
                            "x_link": x_link
                        })
        except Exception as e:
            return {
                "query": stream_label,
                "category": category,
                "country": country,
                "total_articles": 0,
                "error": str(e),
                "articles": []
            }

        # Sort articles by virality score descending for top viral ranking
        viral_ranked = sorted(articles, key=lambda x: x["virality"]["score"], reverse=True)

        return {
            "query": stream_label,
            "category": category,
            "country": country,
            "total_articles": len(articles),
            "articles": articles,
            "most_shared": viral_ranked[:6]
        }

    def generate_client_ad_hooks(self, client_brand: str, client_product: str, client_url: str, trending_headline: str) -> dict:
        """
        Generates contextual news-jacking ad creative angles that bridge
        today's top viral news with a client's product or service.
        """
        brand = client_brand.strip() or "Your Brand"
        product = client_product.strip() or "Premium Solutions"
        url = client_url.strip() or "https://yourwebsite.com"
        headline = trending_headline.strip() or "Market Shifts and Industry Breakout Trends"

        # News-jacking angles
        angle_authority = {
            "angle_name": "👑 The Authority / Safe Harbor Angle",
            "hook": f"While headlines are buzzing about '{headline[:60]}...', industry leaders are choosing stability with {brand}.",
            "body": f"In a fast-changing landscape, don't let market turbulence disrupt your plans. {brand} provides {product} designed for consistent growth and reliability.",
            "cta": f"👉 Discover {brand} Today: {url}"
        }

        angle_opportunity = {
            "angle_name": "🚀 The Opportunity / Wave-Riding Angle",
            "hook": f"Trending Now: '{headline[:55]}...' — How does this impact you?",
            "body": f"Every major industry shift creates unprecedented winners. Upgrade your strategy with {product} from {brand} and stay ahead of the competition.",
            "cta": f"⚡ Claim Exclusive Access at {brand}: {url}"
        }

        angle_fomo = {
            "angle_name": "⚡ The Direct Action / High-Converting Angle",
            "hook": f"Everyone is talking about this news today. But here is what smart operators are doing about it.",
            "body": f"Cut through the noise. Partner with {brand} for {product} and turn breaking market momentum into your unfair advantage.",
            "cta": f"🔥 Get Started with {brand} Now: {url}"
        }

        whatsapp_broadcast = (
            f"📢 *INDUSTRY PULSE & SPONSORED BRIEFING*\n\n"
            f"📌 *Trending Story:* {headline}\n\n"
            f"💡 *Sponsored Spotlight:* Looking for {product}? Partner with *{brand}* for unmatched results and guaranteed support.\n\n"
            f"👉 *Learn More / Book Consultation:* {url}"
        )

        return {
            "angles": [angle_authority, angle_opportunity, angle_fomo],
            "whatsapp_broadcast": whatsapp_broadcast,
            "sponsored_card": {
                "badge": "⭐ SPONSORED TRENDING SPOTLIGHT",
                "client_name": brand,
                "product": product,
                "headline": f"Why {brand} is the Trusted Partner for {product} Amid Shifting Headlines",
                "tagline": f"Specialized solutions engineered for high performance. Trusted by industry innovators.",
                "url": url,
                "cta_text": "Visit Official Portal"
            }
        }
