import streamlit as st
import pandas as pd
from core.traffic_engine import TrafficSpyEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="TrafficSpy | Total Visitors Estimator", page_icon="👥", layout="wide")

st.title("👥 TrafficSpy: Total Website Visitors & Audience Analytics")
st.caption("Dedicated application for estimating monthly web traffic, global rankings, audience bounce rate, and acquisition sources.")

POPULAR_DOMAINS = ["github.com", "openai.com", "apple.com", "netflix.com", "amazon.com", "casagrand.co.in"]

with st.sidebar:
    st.header("👥 Website Selection")
    site_choice = st.selectbox("Popular Websites:", POPULAR_DOMAINS, index=0)
    custom_domain = st.text_input("Or Enter Custom Website:", value="", placeholder="e.g. stripe.com, shopify.com")
    active_domain = custom_domain.strip().lower() if custom_domain else site_choice
    run_btn = st.button("🚀 Check Website Visitors", type="primary", use_container_width=True)

if run_btn or "traffic_active" not in st.session_state:
    with st.spinner(f"Estimating total monthly visitors for {active_domain}..."):
        engine = TrafficSpyEngine()
        data = engine.analyze_traffic(active_domain)
        st.session_state["traffic_data"] = data
        st.session_state["traffic_active"] = active_domain

if "traffic_data" in st.session_state:
    data = st.session_state["traffic_data"]
    dom = st.session_state["traffic_active"]

    # Header & PDF Button
    p_c1, p_c2, p_c3 = st.columns([2, 2, 1])
    with p_c1:
        st.subheader(f"🌐 Traffic Overview: {dom}")
    with p_c2:
        st.metric("Total Monthly Visitors", data["total_monthly_visits"])
    with p_c3:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_traffic_pdf(dom, data)
            if pdf_bytes:
                st.download_button("📄 Export Traffic PDF", pdf_bytes, f"{dom}_Website_Traffic_Report.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")

    # Scorecard Columns
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Global Rank", data["global_rank"])
    with m2:
        st.metric("Country Rank", data["country_rank"])
    with m3:
        st.metric("Bounce Rate", data["bounce_rate"])
    with m4:
        st.metric("Avg Visit Duration", data["avg_visit_duration"])

    st.markdown("---")

    # Traffic Acquisition Breakdown
    c_src, c_geo = st.columns(2)
    with c_src:
        st.markdown("#### 🚦 Traffic Acquisition Channels")
        src_dict = data["traffic_sources"]
        df_src = pd.DataFrame([
            {"Channel": k, "Traffic Share (%)": v}
            for k, v in src_dict.items()
        ])
        st.dataframe(df_src, use_container_width=True, hide_index=True)
        st.bar_chart(df_src.set_index("Channel")["Traffic Share (%)"])

    with c_geo:
        st.markdown("#### 🌍 Top Audience Geographies")
        geo_list = data.get("top_countries", [])
        if geo_list:
            df_geo = pd.DataFrame([
                {"Country Code": g["country_code"], "Traffic Share (%)": g["share_pct"]}
                for g in geo_list
            ])
            st.dataframe(df_geo, use_container_width=True, hide_index=True)
            st.bar_chart(df_geo.set_index("Country Code")["Traffic Share (%)"])
        else:
            st.info("Detailed geographic traffic breakdown protected.")

    st.markdown("---")
    st.write(f"**Pages Per Visit:** `{data['pages_per_visit']}`")
    st.caption(f"Domain notes: {data.get('description', '')}")
