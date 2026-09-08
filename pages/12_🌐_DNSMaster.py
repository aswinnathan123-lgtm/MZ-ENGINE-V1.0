import streamlit as st
import pandas as pd
from core.dns_engine import DNSMasterEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="DNSMaster | Deep DNS & Geolocation", page_icon="🌐", layout="wide")
st.title("🌐 DNSMaster: Deep DNS, WHOIS & Hosting Geolocation")
st.caption("Zero-key DNS-over-HTTPS resolution across A, AAAA, MX, NS, TXT, SOA and reverse ASN IP geolocation.")

with st.sidebar:
    st.header("🌐 Domain Target")
    dom_target = st.text_input("Enter Domain:", value="github.com", placeholder="e.g. stripe.com, openai.com")
    run_btn = st.button("🚀 Resolve DNS Dossier", type="primary", use_container_width=True)

if run_btn or "dns_data" not in st.session_state:
    with st.spinner(f"Resolving DNS & Geolocation for {dom_target}..."):
        engine = DNSMasterEngine()
        data = engine.get_dns_and_ip_dossier(dom_target)
        st.session_state["dns_data"] = data

if "dns_data" in st.session_state:
    data = st.session_state["dns_data"]
    geo = data.get("geo", {})

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        st.subheader(f"🌐 {data['domain']}")
        st.write(f"Primary Server IP: `{data['primary_ip']}`")
    with c2:
        st.metric("Hosting Location", f"{geo.get('city')}, {geo.get('country')}")
    with c3:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_dns_pdf(data["domain"], data)
            if pdf_bytes:
                st.download_button("📄 Export DNS PDF", pdf_bytes, f"{data['domain']}_DNS_Dossier.pdf", "application/pdf", type="primary", use_container_width=True)

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("ISP Provider", geo.get("isp", "N/A")[:20])
    with m2: st.metric("Autonomous System (ASN)", geo.get("asn", "N/A")[:20])
    with m3: st.metric("Organization", geo.get("org", "N/A")[:20])
    with m4: st.metric("Timezone", geo.get("timezone", "UTC"))

    st.markdown("---")
    st.markdown("#### 📋 Resolved DNS Records")
    records = data.get("records", {})
    df_dns = pd.DataFrame([
        {"Record Type": k, "Values": ", ".join(v) if v else "None"}
        for k, v in records.items()
    ])
    st.dataframe(df_dns, use_container_width=True, hide_index=True)
