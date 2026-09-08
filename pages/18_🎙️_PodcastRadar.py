import streamlit as st
from core.podcast_engine import PodcastRadarEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="PodcastRadar | Audio Intelligence", page_icon="🎙️", layout="wide")
st.title("🎙️ PodcastRadar: Apple Podcasts & Creator Audio Discovery")
st.caption("Searches public podcast databases to identify top ranking shows, hosts, episode counts, and RSS feeds.")

with st.sidebar:
    st.header("🎙️ Podcast Query")
    p_query = st.text_input("Niche or Host:", value="AI Startup", placeholder="e.g. Huberman, Lex Fridman, SaaS")
    run_btn = st.button("🚀 Search Podcasts", type="primary", use_container_width=True)

if run_btn or "podcast_data" not in st.session_state:
    with st.spinner(f"Searching shows for '{p_query}'..."):
        engine = PodcastRadarEngine()
        data = engine.search_podcasts(p_query)
        st.session_state["podcast_data"] = data

if "podcast_data" in st.session_state:
    data = st.session_state["podcast_data"]
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.subheader(f"Topic: {data['query']}")
    with c2:
        st.metric("Total Shows Found", data["total_found"])
    with c3:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_podcast_pdf(data["query"], data)
            if pdf_bytes:
                st.download_button("📄 Export Podcast PDF", pdf_bytes, f"{data['query']}_Podcasts.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    for p in data.get("podcasts", []):
        col_img, col_info = st.columns([1, 4])
        with col_img:
            if p["artwork"]:
                st.image(p["artwork"], use_container_width=True)
        with col_info:
            st.markdown(f"### [{p['name']}]({p['itunes_url']})")
            st.write(f"**Host / Artist:** `{p['artist']}` | **Genre:** `{p['primary_genre']}` | **Episodes:** `{p['episodes']}`")
            if p["feed_url"]:
                st.caption(f"RSS Feed: {p['feed_url']}")
        st.markdown("---")
