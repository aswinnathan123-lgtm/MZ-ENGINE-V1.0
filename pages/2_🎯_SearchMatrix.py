import streamlit as st
import pandas as pd
from core.constants import WORLDWIDE_COUNTRIES
from core.predictive_seo import PredictiveSEOEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="SearchMatrix | SEO Demand Engine", page_icon="🎯", layout="wide")

st.title("🎯 SearchMatrix: Real Search Demand & Pincode Radar")
st.caption("Dedicated application for extracting authentic Google & YouTube search demand with hyper-local pincode expansion.")

with st.sidebar:
    st.header("🎯 SearchMatrix Settings")
    keyword = st.text_input("Target Keyword:", value="Construction")
    country = st.selectbox("Country:", list(WORLDWIDE_COUNTRIES.keys()), format_func=lambda k: WORLDWIDE_COUNTRIES[k])
    pincode = st.text_input("Area / Pincode / ZIP:", value="", placeholder="e.g. 560001, 90210")
    alpha_depth = st.slider("Alphabet Soup Depth:", 5, 26, 12)
    run_btn = st.button("🚀 Extract Search Demand", type="primary", use_container_width=True)

if run_btn:
    with st.spinner(f"Ingesting real-time search demand in {WORLDWIDE_COUNTRIES[country]}..."):
        engine = PredictiveSEOEngine(country_code=country, pincode=pincode)
        data = engine.run_deep_matrix(keyword, max_alpha=alpha_depth)
        st.session_state["seo_data"] = data
        st.session_state["seo_kw"] = keyword
        st.session_state["seo_country"] = country
        st.session_state["seo_pin"] = pincode

if "seo_data" in st.session_state:
    data = st.session_state["seo_data"]

    # Header & PDF Button
    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        st.subheader(f"📈 Total Discovered Queries: {data['total_queries_found']}")
    with p_col2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_seo_pdf(
                st.session_state["seo_kw"],
                WORLDWIDE_COUNTRIES[st.session_state["seo_country"]],
                st.session_state["seo_pin"],
                data
            )
            if pdf_bytes:
                st.download_button("📄 Export SearchMatrix PDF", pdf_bytes, f"{st.session_state['seo_kw']}_SearchMatrix.pdf", "application/pdf", type="primary", use_container_width=True)

    if data.get("pincode_localized_queries"):
        st.markdown("#### 📍 Hyper-Local Pincode Search Terms")
        st.write(data["pincode_localized_queries"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 💰 High Buyer-Intent Commercial Queries")
        st.dataframe(pd.DataFrame(data["commercial"], columns=["Commercial Search"]), use_container_width=True, height=280)
    with c2:
        st.markdown("#### ❓ 7W1H Question Hierarchy")
        for cat, q_list in data["questions"].items():
            if q_list:
                with st.expander(f"{cat.upper()} ({len(q_list)} searches)"):
                    st.write(q_list)

    st.markdown("---")
    csv_bytes = pd.DataFrame(data["all_unique_queries"], columns=["Query"]).to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Raw Queries (CSV)", csv_bytes, f"{data['seed']}_queries.csv", "text/csv")
else:
    st.info("👈 Enter your keyword and country, then click 'Extract Search Demand'.")
