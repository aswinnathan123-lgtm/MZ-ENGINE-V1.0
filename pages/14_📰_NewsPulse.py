import streamlit as st
import pandas as pd
from core.news_engine import NewsPulseEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="OmniNews | Universal News Radar", page_icon="📰", layout="wide")
st.title("📰 OmniNews: Universal World & Specialized Media Radar")
st.caption("Covers everything: Global Breaking, India National, Tech & AI, Financial Markets, Defense, and Science with automated headline sentiment analysis.")

CATEGORIES = {
    "🌍 World Breaking": "WORLD",
    "🇮🇳 India National": "NATION",
    "💻 Technology & AI": "TECHNOLOGY",
    "📈 Business & Finance": "BUSINESS",
    "🔬 Science & Space": "SCIENCE",
    "🎬 Entertainment": "ENTERTAINMENT"
}

with st.sidebar:
    st.header("📰 News Category & Search")
    cat_choice = st.selectbox("Select News Category:", list(CATEGORIES.keys()), index=0)
    custom_search = st.text_input("Or Search Any Specific Topic / Brand:", value="", placeholder="e.g. Semiconductor, ISRO, Fed Rates")
    country_sel = st.selectbox("Country Edition:", ["IN", "US", "GB", "CA", "AU"], index=0)
    run_btn = st.button("🚀 Fetch News Feed", type="primary", use_container_width=True)

if run_btn or "omni_news_data" not in st.session_state:
    with st.spinner("Streaming real-time news feeds..."):
        engine = NewsPulseEngine()
        cat_key = CATEGORIES[cat_choice]
        data = engine.fetch_news(query=custom_search, category=cat_key, country=country_sel)
        st.session_state["omni_news_data"] = data

if "omni_news_data" in st.session_state:
    data = st.session_state["omni_news_data"]
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.subheader(f"Stream: {data.get('query', 'Headlines')}")
    with c2:
        st.metric("Total Headlines Found", data.get("total_articles", 0))
    with c3:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_news_pdf(data.get("query", "News"), data)
            if pdf_bytes:
                st.download_button("📄 Export News PDF", pdf_bytes, "OmniNews_Report.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    for a in data.get("articles", []):
        s_color = "🟢" if "POSITIVE" in a["sentiment"] else ("🔴" if "NEGATIVE" in a["sentiment"] else "⚪")
        st.markdown(f"### [{a['title']}]({a['link']})")
        st.write(f"**Source:** `{a['source']}` | **Date:** `{a['pub_date']}` | **Sentiment:** {s_color} `{a['sentiment']}`")
        st.markdown("---")
