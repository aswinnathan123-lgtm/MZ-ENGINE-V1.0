import streamlit as st
from core.speed_engine import SpeedAuditEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="SpeedAudit | Core Web Vitals", page_icon="⚡", layout="wide")
st.title("⚡ SpeedAudit: Google Lighthouse & Core Web Vitals")
st.caption("Leverages Google PageSpeed API to test mobile/desktop load speeds, FCP, LCP, CLS, and TBT.")

with st.sidebar:
    st.header("⚡ Audit Settings")
    site_url = st.text_input("Enter URL:", value="https://stripe.com")
    device_strat = st.radio("Strategy:", ["mobile", "desktop"], index=0)
    run_btn = st.button("🚀 Run Speed Audit", type="primary", use_container_width=True)

if run_btn or "speed_data" not in st.session_state:
    with st.spinner(f"Auditing speed for {site_url}..."):
        engine = SpeedAuditEngine()
        data = engine.run_speed_test(site_url, strategy=device_strat)
        st.session_state["speed_data"] = data

if "speed_data" in st.session_state:
    data = st.session_state["speed_data"]
    if "error" in data:
        st.error(data["error"])
    else:
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.subheader(f"Audited: {data['url']}")
            st.caption(f"Strategy: {data['strategy'].upper()}")
        with c2:
            st.metric("Performance Score", f"{data['performance_score']}/100", data["grade"])
        with c3:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_speed_pdf(data["url"], data)
                if pdf_bytes:
                    st.download_button("📄 Export Speed PDF", pdf_bytes, "SpeedAudit_Report.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("First Contentful Paint (FCP)", data["first_contentful_paint"])
        with m2: st.metric("Largest Contentful Paint (LCP)", data["largest_contentful_paint"])
        with m3: st.metric("Total Blocking Time (TBT)", data["total_blocking_time"])
        with m4: st.metric("Cumulative Layout Shift (CLS)", data["cumulative_layout_shift"])
