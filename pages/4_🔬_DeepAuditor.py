import streamlit as st
import pandas as pd
from core.deep_web_audit import DeepWebAuditor

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="DeepAuditor | Competitor Footprint", page_icon="🔬", layout="wide")

st.title("🔬 DeepAuditor: Competitor Infrastructure & Tech Profiler")
st.caption("Zero-key replacement for SecurityTrails & BuiltWith using Certificate Transparency logs and DOM signatures.")

with st.sidebar:
    st.header("🔬 DeepAuditor Settings")
    domain = st.text_input("Competitor Domain:", value="github.com")
    run_btn = st.button("🚀 Audit Competitor Footprint", type="primary", use_container_width=True)

if run_btn:
    with st.spinner(f"Querying Certificate Transparency logs & DOM for {domain}..."):
        auditor = DeepWebAuditor()
        subs = auditor.get_subdomains_via_cert_transparency(domain, max_limit=40)
        tech = auditor.fingerprint_tech_stack(domain)
        audit_data = {"subdomains": subs, "tech_stack": tech}
        st.session_state["audit_data"] = audit_data
        st.session_state["audit_domain"] = domain

if "audit_data" in st.session_state:
    data = st.session_state["audit_data"]
    dom = st.session_state["audit_domain"]

    p_col1, p_col2 = st.columns([3, 1])
    with p_col1:
        st.subheader(f"Auditing: {dom} | Subdomains Discovered: {data['subdomains'].get('total_found', 0)}")
    with p_col2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_audit_pdf(dom, data)
            if pdf_bytes:
                st.download_button("📄 Export DeepAuditor PDF", pdf_bytes, f"{dom}_DeepAuditor.pdf", "application/pdf", type="primary", use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🛠️ Tech Stack Fingerprint (Zero-Key BuiltWith)")
        t = data["tech_stack"]
        st.write(f"**Web Server:** `{t.get('server', 'N/A')}`")
        st.write(f"**Frameworks:** {', '.join(t.get('frameworks', [])) or 'None detected'}")
        st.write(f"**CMS Platform:** {', '.join(t.get('cms', [])) or 'Custom'}")
        st.write(f"**Analytics & Pixels:** {', '.join(t.get('analytics_and_ads', [])) or 'None'}")
        st.write(f"**CDN & Edge:** {', '.join(t.get('cdn_or_waf', [])) or 'Direct'}")
    with c2:
        st.markdown("#### 🌐 Certificate Transparency Subdomains (crt.sh)")
        subs = data["subdomains"].get("subdomains", [])
        if subs:
            st.dataframe(pd.DataFrame(subs), use_container_width=True, height=280)
        else:
            st.info("No subdomains found or lookup timed out.")
else:
    st.info("👈 Enter a target domain and click 'Audit Competitor Footprint'.")
