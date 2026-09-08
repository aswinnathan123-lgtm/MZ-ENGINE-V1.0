import streamlit as st
from core.brand_engine import BrandForensicsEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="BrandForensics | Brand Assets", page_icon="🎨", layout="wide")
st.title("🎨 BrandForensics: Domain Brand & Visual Asset Extractor")
st.caption("Scrapes target website to extract brand colors, logos, favicons, and social media footprint.")

with st.sidebar:
    st.header("🎨 Target Website")
    target_site = st.text_input("Enter Website URL:", value="apple.com")
    run_btn = st.button("🚀 Extract Assets", type="primary", use_container_width=True)

if run_btn or "brand_data" not in st.session_state:
    with st.spinner(f"Extracting brand assets from {target_site}..."):
        engine = BrandForensicsEngine()
        data = engine.extract_brand_assets(target_site)
        st.session_state["brand_data"] = data

if "brand_data" in st.session_state:
    data = st.session_state["brand_data"]
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader(f"Brand Assets: {data['domain']}")
    with c2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_brand_pdf(data["domain"], data)
            if pdf_bytes:
                st.download_button("📄 Export Brand PDF", pdf_bytes, f"{data['domain']}_BrandAssets.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🎨 Brand Color Palette Detected")
    colors = data.get("brand_colors", [])
    if colors:
        c_cols = st.columns(len(colors))
        for idx, col_hex in enumerate(colors):
            with c_cols[idx]:
                st.markdown(f'<div style="background-color:{col_hex}; height:60px; border-radius:8px; border:1px solid #334155; margin-bottom:4px;"></div>', unsafe_allow_html=True)
                st.caption(col_hex)
    else:
        st.info("No explicit hex colors detected in markup.")

    st.markdown("---")
    st.markdown("#### 🔗 Discovered Social Profiles")
    for s in data.get("social_links", []):
        st.write(f"• [{s}]({s})")
