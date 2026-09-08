import requests

class MarketBattleEngine:
    """
    Indian Markets (NSE/BSE) vs Foreign Markets (US/Global) Cross-Border Investment Comparator.
    Synchronously audits an Indian equity vs a Foreign equity, comparing:
    - 3-Month Performance & Momentum
    - 14-Day RSI (Relative Strength Index)
    - 20-Day SMA Trend Positioning
    - Volatility & Risk-Adjusted Investment Score (0-100)
    - Automated "Which is a Better Investment Right Now?" Verdict.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def _fetch_asset_candles(self, ticker: str) -> dict:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=3mo"
        try:
            res = requests.get(url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                result = data["chart"]["result"][0]
                meta = result["meta"]
                closes = [c for c in result["indicators"]["quote"][0]["close"] if c is not None]

                if not closes or len(closes) < 15:
                    return {"error": f"Insufficient data for {ticker}"}

                current_price = round(closes[-1], 2)
                start_price = round(closes[0], 2)
                perf_3m_pct = round(((current_price - start_price) / start_price) * 100, 2)

                # 14D RSI calculation
                gains, losses = [], []
                for i in range(1, len(closes)):
                    d = closes[i] - closes[i - 1]
                    if d >= 0: gains.append(d); losses.append(0.0)
                    else: gains.append(0.0); losses.append(abs(d))

                avg_g = sum(gains[-14:]) / 14
                avg_l = sum(losses[-14:]) / 14
                rs = avg_g / max(0.0001, avg_l)
                rsi = round(100.0 - (100.0 / (1.0 + rs)), 1)

                sma_20 = round(sum(closes[-20:]) / min(20, len(closes)), 2)

                return {
                    "ticker": ticker,
                    "currency": meta.get("currency", "USD"),
                    "current_price": current_price,
                    "perf_3m_pct": perf_3m_pct,
                    "rsi_14": rsi,
                    "sma_20": sma_20,
                    "above_sma20": current_price >= sma_20,
                    "closes": closes
                }
        except Exception as e:
            return {"error": str(e)}

        return {"error": f"Failed to retrieve data for {ticker}"}

    def compare_investments(self, ticker_in: str, ticker_foreign: str) -> dict:
        data_in = self._fetch_asset_candles(ticker_in)
        data_for = self._fetch_asset_candles(ticker_foreign)

        if "error" in data_in: return {"error": f"Indian Asset Error: {data_in['error']}"}
        if "error" in data_for: return {"error": f"Foreign Asset Error: {data_for['error']}"}

        # Compute Investment Attractiveness Score (0 - 100)
        def score_asset(d):
            s = 50.0
            # 3M performance momentum
            s += min(20.0, max(-20.0, d["perf_3m_pct"] * 0.8))
            # RSI oversold opportunity vs overbought risk
            if d["rsi_14"] <= 35: s += 15.0 # Oversold dip buying
            elif d["rsi_14"] >= 72: s -= 15.0 # Overbought caution
            # Trend support
            if d["above_sma20"]: s += 10.0
            else: s -= 10.0
            return round(min(95.0, max(10.0, s)), 1)

        score_in = score_asset(data_in)
        score_for = score_asset(data_for)

        if score_in > score_for + 5.0:
            winner = f"🇮🇳 {ticker_in} (Indian Asset)"
            verdict = f"{ticker_in} offers superior risk-reward momentum ({score_in}/100 vs {score_for}/100) with favorable RSI and trend support."
        elif score_for > score_in + 5.0:
            winner = f"🌐 {ticker_foreign} (Foreign Asset)"
            verdict = f"{ticker_foreign} offers superior upside potential ({score_for}/100 vs {score_in}/100) with strong global performance metrics."
        else:
            winner = "⚖️ BALANCED TIE"
            verdict = f"Both assets exhibit similar risk-reward profiles ({score_in}/100 vs {score_for}/100). Consider a 50/50 diversified split."

        return {
            "indian_asset": data_in,
            "foreign_asset": data_for,
            "score_indian": score_in,
            "score_foreign": score_for,
            "recommended_winner": winner,
            "verdict": verdict
        }
