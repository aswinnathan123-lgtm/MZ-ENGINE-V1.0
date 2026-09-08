import streamlit as st
import pandas as pd
from core.sherlock_engine import SherlockSocialEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="SherlockSocial | Username Recon", page_icon="🕵️", layout="wide")
st.title("🕵️ SherlockSocial: Multi-Platform Username Reconnaissance")
st.caption("Searches 24+ major social and developer networks in parallel for any handle or username.")

with st.sidebar:
    st.header("🕵️ Target Profile")
    target_user = st.text_input("Enter Username / Handle:", value="torvalds", placeholder="e.g. torvalds, elonmusk, satya")
    run_btn = st.button("🚀 Scan Platforms", type="primary", use_container_width=True)

if run_btn or "sherlock_data" not in st.session_state:
    with st.spinner(f"Scanning 24+ platforms for @{target_user}..."):
        engine = SherlockSocialEngine()
        data = engine.scan_username(target_user)
        st.session_state["sherlock_data"] = data
        st.session_state["sherlock_active"] = target_user

if "sherlock_data" in st.session_state:
    data = st.session_state["sherlock_data"]
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.subheader(f"Target: @{data['username']}")
    with c2:
        st.metric("Presence Rate", f"{data['presence_rate']}%", f"{data['found_count']} / {data['total_scanned']} Found")
    with c3:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_sherlock_pdf(data["username"], data)
            if pdf_bytes:
                st.download_button("📄 Export Sherlock PDF", pdf_bytes, f"{data['username']}_Sherlock_Dossier.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    col_found, col_miss = st.columns(2)
    with col_found:
        st.markdown(f"#### 🟢 Active Profiles Detected ({data['found_count']})")
        for p in data["found_profiles"]:
            st.markdown(f"• **{p['platform']}:** [{p['url']}]({p['url']})")
    with col_miss:
        st.markdown(f"#### ⚪ Available / Not Detected ({len(data['missing_profiles'])})")
        for m in data["missing_profiles"][:10]:
            st.write(f"• {m['platform']}")
