import requests
import json
from datetime import datetime

class StockWatcherEngine:
    """
    Zero-key Stock Market Intelligence Engine.
    Pulls live financial candles, computes RSI, Moving Average crossovers,
    Price Drop Alerts, and calculates Buy Probability Scores (% Chance UP vs DOWN).
    """
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        }

    def _calculate_rsi(self, prices: list, period: int = 14) -> float:
        if len(prices) < period + 1:
            return 50.0
        gains, losses = [], []
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0.0)
            else:
                gains.append(0.0)
                losses.append(abs(diff))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100.0 - (100.0 / (1.0 + rs)), 1)

    def analyze_stock(self, ticker: str) -> dict:
        ticker = ticker.strip().upper()
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=3mo"
        
        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                result = data["chart"]["result"][0]
                meta = result["meta"]
                indicators = result["indicators"]["quote"][0]

                closes = [c for c in indicators["close"] if c is not None]
                volumes = [v for v in indicators["volume"] if v is not None]

                if not closes:
                    return {"error": f"No price data available for ticker '{ticker}'"}

                current_price = round(closes[-1], 2)
                prev_close = round(meta.get("chartPreviousClose", closes[-2] if len(closes) > 1 else current_price), 2)
                change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)

                # Technical Calculations
                rsi = self._calculate_rsi(closes, 14)
                sma_20 = round(sum(closes[-20:]) / min(20, len(closes)), 2)
                sma_50 = round(sum(closes[-50:]) / min(50, len(closes)), 2) if len(closes) >= 50 else sma_20

                # 1. Price Drop Alert Detection
                if change_pct <= -5.0:
                    drop_alert = "🚨 HIGH ALERT: Severe Price Drop (-5%+). Potential Oversold Bounce Zone."
                    alert_level = "CRITICAL"
                elif change_pct <= -2.5:
                    drop_alert = "⚠️ MODERATE ALERT: Pullback in progress (-2.5%+)."
                    alert_level = "WARNING"
                elif change_pct >= 3.0:
                    drop_alert = "🚀 BULLISH SURGE: Gaining upward momentum (+3%+)."
                    alert_level = "BULLISH"
                else:
                    drop_alert = "🟢 STABLE: Normal trading range."
                    alert_level = "NORMAL"

                # 2. Probability Score to go UP vs DOWN (0% to 100%)
                prob_score = 50.0
                signals = []

                # RSI Factor
                if rsi <= 32:
                    prob_score += 22.0
                    signals.append(f"RSI is oversold at {rsi} (Strong technical bounce signal)")
                elif rsi >= 68:
                    prob_score -= 22.0
                    signals.append(f"RSI is overbought at {rsi} (Cool-off risk)")
                else:
                    signals.append(f"RSI is neutral at {rsi}")

                # Trend / Moving Average Factor
                if current_price > sma_20:
                    prob_score += 15.0
                    signals.append(f"Trading above 20-day SMA (${sma_20})")
                else:
                    prob_score -= 15.0
                    signals.append(f"Trading below 20-day SMA (${sma_20})")

                if sma_20 > sma_50:
                    prob_score += 10.0
                    signals.append("Golden slope: 20-day SMA above 50-day SMA")
                else:
                    prob_score -= 10.0
                    signals.append("Bearish slope: 20-day SMA below 50-day SMA")

                # Recent dip opportunity boost
                if change_pct < -3.0 and rsi < 45:
                    prob_score += 10.0
                    signals.append("Dip discount: Pullback with room to recover")

                prob_up = min(95.0, max(5.0, round(prob_score, 1)))
                prob_down = round(100.0 - prob_up, 1)

                if prob_up >= 65.0:
                    verdict = "STRONG BUY PROBABILITY (Bullish Setup)"
                elif prob_up >= 55.0:
                    verdict = "MODERATE BUY (Mild Upward Bias)"
                elif prob_up <= 35.0:
                    verdict = "HIGH DROP RISK (Bearish Pressure)"
                else:
                    verdict = "NEUTRAL / SIDEWAYS CONSOLIDATION"

                return {
                    "ticker": ticker,
                    "currency": meta.get("currency", "USD"),
                    "current_price": current_price,
                    "previous_close": prev_close,
                    "change_pct": change_pct,
                    "sma_20": sma_20,
                    "sma_50": sma_50,
                    "rsi_14": rsi,
                    "drop_alert": drop_alert,
                    "alert_level": alert_level,
                    "prob_up": prob_up,
                    "prob_down": prob_down,
                    "verdict": verdict,
                    "signals": signals,
                    "recent_closes": closes[-15:]
                }
        except Exception as e:
            return {"error": f"Failed to fetch stock data for '{ticker}': {str(e)}"}

        return {"error": f"Invalid stock ticker or server timeout."}
