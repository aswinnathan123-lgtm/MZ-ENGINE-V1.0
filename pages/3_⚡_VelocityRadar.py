import streamlit as st
import pandas as pd
from core.constants import WORLDWIDE_COUNTRIES
from core.video_forensics import VideoForensicsEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="VelocityRadar | Video Momentum", page_icon="⚡", layout="wide")

st.title("⚡ VelocityRadar: YouTube Views-Per-Hour (VPH) Tracker")
st.caption("Dedicated application for calculating real-time breakout momentum and Views-Per-Hour without API keys.")

with st.sidebar:
    st.header("⚡ VelocityRadar Settings")
    topic = st.text_input("Video Topic / Keyword:", value="Construction")
    country = st.selectbox("Country:", list(WORLDWIDE_COUNTRIES.keys()), format_func=lambda k: WORLDWIDE_COUNTRIES[k])
    max_vids = st.slider("Videos to Audit:", 10, 35, 20)
    run_btn = st.button("🚀 Calculate Video Velocity", type="primary", use_container_width=True)

if run_btn:
    with st.spinner(f"Computing real-time VPH in {WORLDWIDE_COUNTRIES[country]}..."):
        engine = VideoForensicsEngine(country_code=country)
        data = engine.fetch_localized_youtube_radar(topic, limit=max_vids)
        st.session_state["vph_data"] = data
        st.session_state["vph_topic"] = topic

if "vph_data" in st.session_state:
    data = st.session_state["vph_data"]

    # Header & PDF Button
    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        st.metric("Average Velocity", f"{data['average_vph']} VPH")
    with p_col2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_velocity_pdf(st.session_state["vph_topic"], data)
            if pdf_bytes:
                st.download_button("📄 Export VelocityRadar PDF", pdf_bytes, f"{st.session_state['vph_topic']}_VelocityRadar.pdf", "application/pdf", type="primary", use_container_width=True)

    v_list = data["videos"]
    if v_list:
        df_v = pd.DataFrame([
            {
                "Title": v["title"],
                "Velocity (VPH)": v["vph"],
                "Views": v["views_formatted"] or v["views"],
                "Channel": v["channel"],
                "Hook": v["hook"],
                "URL": v["url"]
            }
            for v in v_list
        ])
        st.dataframe(df_v, use_container_width=True, height=400)

        top_v = data.get("top_breakout_video")
        if top_v:
            st.markdown("---")
            st.info(f"🔥 **Top Breakout Video:** {top_v['title']}\n\n**Velocity:** {top_v['vph']} VPH | **Channel:** {top_v['channel']} | **Hook Type:** {top_v['hook']}")
else:
    st.info("👈 Enter your topic, then click 'Calculate Video Velocity'.")
