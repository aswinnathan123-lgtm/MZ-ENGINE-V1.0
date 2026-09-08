import streamlit as st
import pandas as pd
from core.constants import WORLDWIDE_COUNTRIES, CREATOR_PERSONAS, ELITE_6_HOOKS
from core.video_forensics import VideoForensicsEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="HookStudio | 6-Hook Intelligence", page_icon="🪝", layout="wide")

st.title("🪝 HookStudio: Viral 6-Hook Dominance Engine")
st.caption("Dedicated application for analyzing which of the 6 Elite Hook Archetypes is winning in your target country.")

with st.sidebar:
    st.header("🪝 HookStudio Settings")
    topic = st.text_input("Niche / Content Topic:", value="Construction")
    country = st.selectbox("Target Country:", list(WORLDWIDE_COUNTRIES.keys()), format_func=lambda k: WORLDWIDE_COUNTRIES[k])
    max_vids = st.slider("Videos to Analyze:", min_value=10, max_value=40, value=25)
    run_btn = st.button("🚀 Analyze Local Hooks", type="primary", use_container_width=True)

if run_btn:
    with st.spinner(f"Scanning local video hooks in {WORLDWIDE_COUNTRIES[country]}..."):
        engine = VideoForensicsEngine(country_code=country)
        data = engine.fetch_localized_youtube_radar(topic, limit=max_vids)
        st.session_state["hook_data"] = data
        st.session_state["hook_topic"] = topic
        st.session_state["hook_country"] = country

if "hook_data" in st.session_state:
    data = st.session_state["hook_data"]
    h_shares = data["hook_dominance"]

    # Header & PDF Button
    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        st.subheader(f"📊 Hook Market Share: '{st.session_state['hook_topic']}' in {WORLDWIDE_COUNTRIES[st.session_state['hook_country']]}")
    with p_col2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_hook_pdf(
                st.session_state["hook_topic"],
                WORLDWIDE_COUNTRIES[st.session_state["hook_country"]],
                h_shares,
                data["videos"]
            )
            if pdf_bytes:
                st.download_button("📄 Export HookStudio PDF", pdf_bytes, f"{st.session_state['hook_topic']}_HookStudio.pdf", "application/pdf", type="primary", use_container_width=True)

    # Visualization
    hook_df = pd.DataFrame([
        {"Hook Archetype": k, "Market Share (%)": v["percentage"], "Count": v["count"]}
        for k, v in h_shares.items()
    ]).sort_values(by="Market Share (%)", ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        st.dataframe(hook_df, use_container_width=True, hide_index=True)
    with c2:
        st.bar_chart(hook_df.set_index("Hook Archetype")["Market Share (%)"])

    st.markdown("---")
    st.subheader("🏆 The 6 Elite Hook Archetypes Playbook")
    for h_name, h_info in ELITE_6_HOOKS.items():
        with st.expander(f"✨ {h_name}"):
            st.write(f"**Description:** {h_info['description']}")
            st.write(f"**Proven Template:** *\"{h_info['example']}\"*")
            matched = [v["title"] for v in data["videos"] if v["hook"] == h_name]
            if matched:
                st.markdown("**Sample Detected Videos:**")
                for m in matched[:3]:
                    st.write(f" • {m}")
else:
    st.info("👈 Enter your topic and country in the sidebar, then click 'Analyze Local Hooks'.")
