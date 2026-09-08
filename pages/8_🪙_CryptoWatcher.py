import streamlit as st
import pandas as pd
from core.crypto_engine import CryptoWatcherEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="CryptoWatcher | Digital Assets", page_icon="🪙", layout="wide")

st.title("🪙 CryptoWatcher: 24h Volatility & Dip-Buy Probability Engine")
st.caption("Dedicated application for monitoring cryptocurrency spot prices, 24h flash crash / drop alerts, and statistical bounce probability scores.")

POPULAR_COINS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "ADA", "AVAX", "LINK", "SUI", "PEPE", "NEAR"]

with st.sidebar:
    st.header("🪙 Crypto Selection")
    coin_choice = st.selectbox("Popular Cryptocurrencies:", POPULAR_COINS, index=0)
    custom_coin = st.text_input("Or Enter Custom Symbol:", value="", placeholder="e.g. RENDER, INJ, TIA")
    active_coin = custom_coin.strip().upper() if custom_coin else coin_choice
    run_btn = st.button("🚀 Analyze Crypto Momentum", type="primary", use_container_width=True)

if run_btn or "crypto_active" not in st.session_state:
    with st.spinner(f"Querying real-time liquidity for {active_coin}/USDT..."):
        engine = CryptoWatcherEngine()
        data = engine.analyze_crypto(active_coin)
        st.session_state["crypto_data"] = data
        st.session_state["crypto_active"] = active_coin

if "crypto_data" in st.session_state:
    data = st.session_state["crypto_data"]
    coin = st.session_state["crypto_active"]

    if "error" in data:
        st.error(data["error"])
    else:
        # Header & PDF Button
        p_c1, p_c2, p_c3 = st.columns([2, 2, 1])
        with p_c1:
            st.subheader(f"🪙 {coin}/USDT Market Overview")
        with p_c2:
            color = "green" if data["change_24h_pct"] >= 0 else "red"
            st.markdown(f"### ${data['price']:,.4f} <span style='color:{color}; font-size:18px;'>({data['change_24h_pct']:+.2f}%)</span>", unsafe_allow_html=True)
        with p_c3:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_crypto_pdf(coin, data)
                if pdf_bytes:
                    st.download_button("📄 Export Crypto PDF", pdf_bytes, f"{coin}_Crypto_Intelligence.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")

        # Probability Meter & Drop Alert
        col_prob, col_alert = st.columns(2)
        with col_prob:
            st.markdown("#### 🎯 Buy Probability Score (Next Move)")
            m_up, m_down = st.columns(2)
            with m_up:
                st.metric("Probability to Go UP 🚀", f"{data['prob_up']}%")
            with m_down:
                st.metric("Probability to Go DOWN 📉", f"{data['prob_down']}%")
            
            st.progress(data['prob_up'] / 100.0)
            st.info(f"**Sentiment Verdict:** {data['verdict']}")

        with col_alert:
            st.markdown("#### 🚨 Crypto Drop & Flash Crash Alert")
            if data["alert_level"] == "CRITICAL":
                st.error(data["drop_alert"])
            elif data["alert_level"] == "WARNING":
                st.warning(data["drop_alert"])
            elif data["alert_level"] == "BULLISH":
                st.success(data["drop_alert"])
            else:
                st.info(data["drop_alert"])

            st.write(f"**24h Range:** `${data['low_24h']:,.4f}` (Low) — `${data['high_24h']:,.4f}` (High)")
            st.write(f"**24h Volume:** `${data['volume_usd']:,.0f} USDT`")

        st.markdown("---")
        st.markdown("#### 🔍 On-Chain & Price Action Signals")
        for sig in data["signals"]:
            st.write(f"• {sig}")
