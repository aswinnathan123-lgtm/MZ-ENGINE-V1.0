import requests
import json

class CryptoWatcherEngine:
    """
    Zero-key Cryptocurrency Intelligence Engine.
    Queries real-time spot tickers, computes 24h volatility, Flash Crash / Drop Alerts,
    and calculates Buy Probability Scores (% Chance UP vs DOWN).
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def analyze_crypto(self, symbol: str) -> dict:
        symbol = symbol.strip().upper().replace("USDT", "").replace("USD", "")
        pair = f"{symbol}USDT"
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={pair}"

        try:
            res = requests.get(url, headers=self.headers, timeout=6)
            if res.status_code == 200:
                data = res.json()

                current_price = float(data.get("lastPrice", 0))
                price_change_pct = float(data.get("priceChangePercent", 0))
                high_24h = float(data.get("highPrice", 0))
                low_24h = float(data.get("lowPrice", 0))
                volume_base = float(data.get("volume", 0))
                volume_quote = float(data.get("quoteVolume", 0))

                # 1. Crypto Drop Alert
                if price_change_pct <= -8.0:
                    drop_alert = "🚨 FLASH CRASH / MASSIVE DIP (-8%+): High risk / high reward bounce zone."
                    alert_level = "CRITICAL"
                elif price_change_pct <= -4.0:
                    drop_alert = "⚠️ PULLBACK ALERT (-4%+): Corrective wave in progress."
                    alert_level = "WARNING"
                elif price_change_pct >= 8.0:
                    drop_alert = "🚀 PUMP ALERT (+8%+): Strong upside breakout / high volume expansion."
                    alert_level = "BULLISH"
                else:
                    drop_alert = "🟢 NORMAL RANGE: Healthy trading consolidation."
                    alert_level = "NORMAL"

                # 2. Probability Score to Go UP vs DOWN
                prob_score = 50.0
                signals = []

                # Proximity to 24h Low vs High
                price_range = max(0.00001, high_24h - low_24h)
                pos_in_range = (current_price - low_24h) / price_range  # 0.0 (near bottom) to 1.0 (near top)

                if pos_in_range < 0.25:
                    prob_score += 20.0
                    signals.append(f"Testing 24h Support: Trading in lower 25% of daily range (${low_24h:,.4f})")
                elif pos_in_range > 0.85:
                    prob_score -= 15.0
                    signals.append(f"Testing 24h Resistance: Trading in top 15% of daily range (${high_24h:,.4f})")
                else:
                    signals.append("Trading in mid-range channel")

                # Volatility Momentum
                if price_change_pct < -5.0 and pos_in_range < 0.3:
                    prob_score += 15.0
                    signals.append("Oversold exhaustion: Dip buying opportunity")
                elif price_change_pct > 10.0:
                    prob_score -= 10.0
                    signals.append("Overextended rally: Short-term profit taking risk")

                # High volume confirmation
                if volume_quote > 50_000_000:
                    signals.append("Institutional liquidity: >$50M 24h volume")

                prob_up = min(92.0, max(8.0, round(prob_score, 1)))
                prob_down = round(100.0 - prob_up, 1)

                if prob_up >= 65.0:
                    verdict = "BULLISH ACCUMULATION (High Bounce Probability)"
                elif prob_up >= 55.0:
                    verdict = "MILD BULLISH BIAS"
                elif prob_up <= 38.0:
                    verdict = "BEARISH CONTINUATION RISK (Downward Pressure)"
                else:
                    verdict = "RANGE-BOUND NEUTRAL"

                return {
                    "symbol": symbol,
                    "pair": pair,
                    "price": current_price,
                    "change_24h_pct": price_change_pct,
                    "high_24h": high_24h,
                    "low_24h": low_24h,
                    "volume_usd": volume_quote,
                    "drop_alert": drop_alert,
                    "alert_level": alert_level,
                    "prob_up": prob_up,
                    "prob_down": prob_down,
                    "verdict": verdict,
                    "signals": signals
                }
        except Exception as e:
            return {"error": f"Failed to fetch crypto ticker for '{symbol}': {str(e)}"}

        return {"error": f"Crypto pair '{symbol}USDT' not found or Binance API timeout."}
