import streamlit as st
from core.breach_engine import BreachRadarEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="BreachRadar | Security Exposure", page_icon="🛡️", layout="wide")
st.title("🛡️ BreachRadar: Credential & Security Exposure Intelligence")
st.caption("Checks password leak frequency across 800M+ real-world compromised breach dumps using NIST k-Anonymity.")

with st.sidebar:
    st.header("🛡️ Security Check")
    pwd_check = st.text_input("Enter Password to Test:", value="Password123!", type="password")
    run_btn = st.button("🚀 Verify Exposure", type="primary", use_container_width=True)

if run_btn or "breach_data" not in st.session_state:
    with st.spinner("Checking breach directories via k-Anonymity..."):
        engine = BreachRadarEngine()
        data = engine.check_password_exposure(pwd_check)
        st.session_state["breach_data"] = data
        st.session_state["breach_target"] = "[Confidential Password Hash]"

if "breach_data" in st.session_state:
    data = st.session_state["breach_data"]
    if "error" in data:
        st.error(data["error"])
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            if data["compromised"]:
                st.error(data["verdict"])
                st.metric("Times Leaked in Public Breaches", f"{data['times_seen']:,}")
            else:
                st.success(data["verdict"])
                st.metric("Times Leaked", "0 (Clean)")
        with c2:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_breach_pdf("Password Exposure Check", data)
                if pdf_bytes:
                    st.download_button("📄 Export Breach PDF", pdf_bytes, "Breach_Audit_Report.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown("##### 🔒 Privacy & Cryptography Note:")
        st.caption("Your password is never transmitted across the network. Only the first 5 characters of its SHA-1 hash are queried against the NIST k-Anonymity protocol.")
