import streamlit as st
import pandas as pd
from core.constants import CREATOR_PERSONAS
from core.social_radar import SocialRadarEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="PainPointRadar | Customer Voice", page_icon="🌊", layout="wide")

st.title("🌊 PainPointRadar: Unfiltered Customer Objections & Audio")
st.caption("Dedicated application for extracting real buyer struggles from Reddit discussions matched with high-retention audio templates.")

with st.sidebar:
    st.header("🌊 PainPointRadar Settings")
    topic = st.text_input("Niche / Industry:", value="Construction")
    creator = st.selectbox("Creator Persona:", list(CREATOR_PERSONAS.keys()), format_func=lambda k: CREATOR_PERSONAS[k]["name"])
    run_btn = st.button("🚀 Intercept Customer Objections", type="primary", use_container_width=True)

if run_btn:
    with st.spinner("Extracting unfiltered discussions and sound pacing..."):
        engine = SocialRadarEngine()
        pain = engine.get_community_pain_points(topic, limit=12)
        audio = engine.get_persona_audio_formulas(creator)
        st.session_state["pain_data"] = pain
        st.session_state["audio_data"] = audio
        st.session_state["pain_topic"] = topic

if "pain_data" in st.session_state:
    pain = st.session_state["pain_data"]
    audio = st.session_state["audio_data"]
    top = st.session_state["pain_topic"]

    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        st.subheader(f"💬 Found {len(pain)} Real Customer Objections for '{top}'")
    with p_col2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_painpoint_pdf(top, pain, audio)
            if pdf_bytes:
                st.download_button("📄 Export PainPoint PDF", pdf_bytes, f"{top}_PainPoints.pdf", "application/pdf", type="primary", use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🗣️ Real Audience Problems & Complaints")
        for p in pain:
            st.info(f"**{p['title']}**\n\n{p['snippet']}\n\n[Open Thread]({p['link']})")
    with c2:
        st.markdown("#### 🎵 High-Retention Audio & Pacing Templates")
        for a in audio:
            st.write(f"🎧 **{a['sound']}**")
            st.caption(f"Pacing: {a['pacing']} • Impact: {a['retention']}")
else:
    st.info("👈 Enter your niche and click 'Intercept Customer Objections'.")
