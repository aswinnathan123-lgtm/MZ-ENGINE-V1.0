import streamlit as st
import pandas as pd
from core.adspy_engine import AdSpyEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="AdSpy | Paid Ads Intelligence", page_icon="📱", layout="wide")
st.title("📱 AdSpy: Paid Traffic & Social Ad Intelligence")
st.caption("Deep-links into Meta Ad Library & Google Ads Transparency to reverse-engineer competitor campaigns and ad angles.")

with st.sidebar:
    st.header("📱 Brand or Keyword")
    brand_target = st.text_input("Brand / Product:", value="Shopify", placeholder="e.g. Nike, HubSpot, Canva")
    run_btn = st.button("🚀 Generate Ad Dossier", type="primary", use_container_width=True)

if run_btn or "adspy_data" not in st.session_state:
    engine = AdSpyEngine()
    data = engine.analyze_ads(brand_target)
    st.session_state["adspy_data"] = data

if "adspy_data" in st.session_state:
    data = st.session_state["adspy_data"]
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader(f"Competitor Paid Ad Channels: {data['target']}")
    with c2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_adspy_pdf(data["target"], data)
            if pdf_bytes:
                st.download_button("📄 Export AdSpy PDF", pdf_bytes, f"{data['target']}_AdSpy_Report.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔗 Direct Competitor Live Ad Vaults")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.link_button("📘 View Meta / FB Ad Library", data["meta_ad_library_url"], type="primary", use_container_width=True)
    with b2:
        st.link_button("🔍 View Google Ads Transparency", data["google_ad_transparency_url"], use_container_width=True)
    with b3:
        st.link_button("🎵 View TikTok Creative Center", data["tiktok_creative_center_url"], use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💡 High-Converting Ad Creative Angles")
    df_angles = pd.DataFrame(data["suggested_ad_creative_angles"])
    st.dataframe(df_angles, use_container_width=True, hide_index=True)
