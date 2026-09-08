import streamlit as st
import pandas as pd
from core.finance_engine import StockWatcherEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="StockWatcher | Equities Intelligence", page_icon="📈", layout="wide")

st.title("📈 StockWatcher: Real-Time Price Drops & Buy Probability Score")
st.caption("Dedicated application for monitoring stocks, RSI oversold bounces, price drop alerts, and statistical buy probability scores.")

POPULAR_STOCKS = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN", "GOOGL", "META", "RELIANCE.NS", "TCS.NS", "INFY.NS", "SPY", "QQQ"]

with st.sidebar:
    st.header("📈 Stock Selection")
    stock_choice = st.selectbox("Popular Stocks:", POPULAR_STOCKS, index=1)
    custom_ticker = st.text_input("Or Enter Custom Ticker:", value="", placeholder="e.g. AMD, PLTR, TATAMOTORS.NS")
    active_ticker = custom_ticker.strip().upper() if custom_ticker else stock_choice
    run_btn = st.button("🚀 Analyze Stock Momentum", type="primary", use_container_width=True)

if run_btn or "stock_active" not in st.session_state:
    with st.spinner(f"Analyzing real-time market data for {active_ticker}..."):
        engine = StockWatcherEngine()
        data = engine.analyze_stock(active_ticker)
        st.session_state["stock_data"] = data
        st.session_state["stock_active"] = active_ticker

if "stock_data" in st.session_state:
    data = st.session_state["stock_data"]
    ticker = st.session_state["stock_active"]

    if "error" in data:
        st.error(data["error"])
    else:
        # Header & PDF Button
        p_c1, p_c2, p_c3 = st.columns([2, 2, 1])
        with p_c1:
            st.subheader(f"📊 {ticker} Market Overview")
        with p_c2:
            color = "green" if data["change_pct"] >= 0 else "red"
            st.markdown(f"### ${data['current_price']} {data['currency']} <span style='color:{color}; font-size:18px;'>({data['change_pct']}%)</span>", unsafe_allow_html=True)
        with p_c3:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_stock_pdf(ticker, data)
                if pdf_bytes:
                    st.download_button("📄 Export Stock PDF", pdf_bytes, f"{ticker}_Stock_Intelligence.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")

        # Probability Meter & Drop Alert
        col_prob, col_alert = st.columns(2)
        with col_prob:
            st.markdown("#### 🎯 Probability Score (Next Move)")
            m_up, m_down = st.columns(2)
            with m_up:
                st.metric("Probability to Go UP 🚀", f"{data['prob_up']}%")
            with m_down:
                st.metric("Probability to Go DOWN 📉", f"{data['prob_down']}%")
            
            # Visual Progress
            st.progress(data['prob_up'] / 100.0)
            st.info(f"**Market Verdict:** {data['verdict']}")

        with col_alert:
            st.markdown("#### 🚨 Price Drop & Dip Alert Status")
            if data["alert_level"] == "CRITICAL":
                st.error(data["drop_alert"])
            elif data["alert_level"] == "WARNING":
                st.warning(data["drop_alert"])
            elif data["alert_level"] == "BULLISH":
                st.success(data["drop_alert"])
            else:
                st.info(data["drop_alert"])

            st.write(f"**14-Day RSI:** `{data['rsi_14']}` (Oversold < 30 | Overbought > 70)")
            st.write(f"**20-Day SMA:** `${data['sma_20']}` | **50-Day SMA:** `${data['sma_50']}`")

        # Technical Signals
        st.markdown("---")
        st.markdown("#### 🔍 Technical Indicators Triggered")
        for sig in data["signals"]:
            st.write(f"• {sig}")

        # Recent Closes Chart
        if data.get("recent_closes"):
            st.markdown("---")
            st.markdown("#### 📉 Recent 15-Day Price Trend")
            df_chart = pd.DataFrame(data["recent_closes"], columns=["Closing Price ($)"])
            st.line_chart(df_chart)
