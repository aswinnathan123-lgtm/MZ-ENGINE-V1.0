import streamlit as st
from core.company_engine import CompanyIntelEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="CompanyIntel | Corporate Profile", page_icon="💼", layout="wide")
st.title("💼 CompanyIntel: Corporate & Enterprise Intelligence")
st.caption("Pulls verified corporate backgrounds, executive overviews, and entity records without subscription paywalls.")

with st.sidebar:
    st.header("💼 Company Target")
    c_target = st.text_input("Company Name:", value="Nvidia", placeholder="e.g. OpenAI, Tesla, Microsoft, Stripe")
    run_btn = st.button("🚀 Retrieve Dossier", type="primary", use_container_width=True)

if run_btn or "company_data" not in st.session_state:
    with st.spinner(f"Gathering intel on {c_target}..."):
        engine = CompanyIntelEngine()
        data = engine.get_company_dossier(c_target)
        st.session_state["company_data"] = data

if "company_data" in st.session_state:
    data = st.session_state["company_data"]
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader(f"🏢 {data.get('title', data.get('company'))}")
        st.caption(f"Category: {data.get('description')}")
    with c2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_company_pdf(data.get("company", "Company"), data)
            if pdf_bytes:
                st.download_button("📄 Export Company PDF", pdf_bytes, f"{data.get('company')}_Corporate_Dossier.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    st.write(data.get("extract"))
    if data.get("page_url"):
        st.markdown(f"🔗 [Read Full Verified Entity Documentation]({data['page_url']})")
