import streamlit as st
import pandas as pd
from core.market_battle_engine import MarketBattleEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="MarketBattle | India vs Foreign Investments", page_icon="⚔️", layout="wide")
st.title("⚔️ MarketBattle: Indian Markets vs Foreign Markets Investment Arbitrage")
st.caption("Head-to-head live investment comparison: Nifty/Sensex & Indian Equities vs S&P 500/Nasdaq & US Giants with an algorithmic 'Which One to Buy?' verdict.")

INDIAN_ASSETS = [
    ("^NSEI", "Nifty 50 Index"),
    ("^BSESN", "BSE Sensex Index"),
    ("RELIANCE.NS", "Reliance Industries"),
    ("TCS.NS", "Tata Consultancy Services"),
    ("HDFCBANK.NS", "HDFC Bank"),
    ("TATAMOTORS.NS", "Tata Motors"),
    ("INFY.NS", "Infosys")
]

FOREIGN_ASSETS = [
    ("^GSPC", "S&P 500 Index"),
    ("^IXIC", "Nasdaq Composite"),
    ("NVDA", "Nvidia Corp"),
    ("AAPL", "Apple Inc"),
    ("MSFT", "Microsoft"),
    ("TSLA", "Tesla Inc"),
    ("GOOGL", "Alphabet / Google")
]

with st.sidebar:
    st.header("⚔️ Asset Matchup")
    in_sel = st.selectbox("Select Indian Asset:", [t[0] for t in INDIAN_ASSETS], index=0)
    for_sel = st.selectbox("Select Foreign Asset:", [t[0] for t in FOREIGN_ASSETS], index=0)
    run_btn = st.button("🚀 Battle Test Investments", type="primary", use_container_width=True)

if run_btn or "battle_data" not in st.session_state:
    with st.spinner(f"Comparing {in_sel} vs {for_sel}..."):
        engine = MarketBattleEngine()
        data = engine.compare_investments(in_sel, for_sel)
        st.session_state["battle_data"] = data

if "battle_data" in st.session_state:
    data = st.session_state["battle_data"]
    if "error" in data:
        st.error(data["error"])
    else:
        d_in = data["indian_asset"]
        d_us = data["foreign_asset"]

        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"🏆 Recommended: {data['recommended_winner']}")
            st.info(data["verdict"])
        with c2:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_market_battle_pdf(d_in["ticker"], d_us["ticker"], data)
                if pdf_bytes:
                    st.download_button("📄 Export Battle PDF", pdf_bytes, f"{d_in['ticker']}_vs_{d_us['ticker']}_Battle.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")
        col_in, col_us = st.columns(2)
        with col_in:
            st.markdown(f"### 🇮🇳 {d_in['ticker']}")
            st.metric("Current Price", f"{d_in['current_price']} {d_in['currency']}")
            st.metric("3-Month Return", f"{d_in['perf_3m_pct']}%")
            st.metric("14-Day RSI", d_in["rsi_14"])
            st.metric("Investment Score", f"{data['score_indian']}/100")
            st.caption(f"20-Day SMA: {d_in['sma_20']} | Trading {'ABOVE' if d_in['above_sma20'] else 'BELOW'} SMA")

        with col_us:
            st.markdown(f"### 🌐 {d_us['ticker']}")
            st.metric("Current Price", f"{d_us['current_price']} {d_us['currency']}")
            st.metric("3-Month Return", f"{d_us['perf_3m_pct']}%")
            st.metric("14-Day RSI", d_us["rsi_14"])
            st.metric("Investment Score", f"{data['score_foreign']}/100")
            st.caption(f"20-Day SMA: {d_us['sma_20']} | Trading {'ABOVE' if d_us['above_sma20'] else 'BELOW'} SMA")

        st.markdown("---")
        st.markdown("#### 📊 3-Month Closing Price Trajectory")
        chart_df = pd.DataFrame({
            f"🇮🇳 {d_in['ticker']} (Normalized %)": [(p/d_in['closes'][0] - 1)*100 for p in d_in['closes']],
            f"🌐 {d_us['ticker']} (Normalized %)": [(p/d_us['closes'][0] - 1)*100 for p in d_us['closes']]
        })
        st.line_chart(chart_df)
