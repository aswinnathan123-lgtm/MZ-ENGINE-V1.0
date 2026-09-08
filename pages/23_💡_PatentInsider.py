import streamlit as st
import pandas as pd
from core.patent_engine import PatentInsiderEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="PatentInsider | Stealth R&D & Tech Inventions", page_icon="💡", layout="wide")
st.title("💡 PatentInsider: Corporate Patent Surveillance & Stealth Tech Radar")
st.caption("Tracks confidential patent applications filed by tech and industrial giants (Apple, Tesla, Nvidia, Tata, Reliance) to uncover next-gen tech before product launches.")

POPULAR_COMPANIES = ["Apple", "Tesla", "Nvidia", "Tata", "Reliance", "Microsoft", "Alphabet"]

with st.sidebar:
    st.header("💡 Corporate Target")
    c_choice = st.selectbox("Monitored Giants:", POPULAR_COMPANIES, index=0)
    custom_c = st.text_input("Or Enter Company/Assignee:", value="")
    active_c = custom_c.strip() if custom_c else c_choice
    run_btn = st.button("🚀 Search Patent Inventions", type="primary", use_container_width=True)

if run_btn or "patent_data" not in st.session_state:
    with st.spinner(f"Tracking patent filings for {active_c}..."):
        engine = PatentInsiderEngine()
        data = engine.search_patents(active_c)
        st.session_state["patent_data"] = data

if "patent_data" in st.session_state:
    data = st.session_state["patent_data"]
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.subheader(f"🏢 {data['company']} Patent Intelligence")
    with c2:
        st.metric("Tracked Breakthrough Filings", data["total_patents_tracked"])
    with c3:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_patent_pdf(data["company"], data)
            if pdf_bytes:
                st.download_button("📄 Export Patent PDF", pdf_bytes, f"{data['company']}_Patent_Dossier.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    st.link_button(f"🔍 Open Live Google Patents Database for {data['company']}", data["google_patents_url"], type="primary")

    st.markdown("---")
    st.markdown("#### 🔬 Recently Published Stealth Inventions & Applications")
    for p in data.get("patents", []):
        st.markdown(f"### 📑 `{p['id']}`: {p['title']}")
        st.write(f"• **Tech Domain:** `{p.get('domain', 'R&D')}` | **Filing/Publication:** `{p.get('filed', 'Recent')}`")
        st.markdown("---")
