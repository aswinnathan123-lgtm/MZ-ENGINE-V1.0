import pandas as pd
import streamlit as st

from core.job_engine import JobRadarEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

st.set_page_config(page_title="JobRadar | All-India Package Intelligence", page_icon="💼", layout="wide")
st.title("💼 JobRadar: All-India Fast Job & Package Intelligence")
st.caption("LinkedIn, Naukri, Indeed, Foundit, and Wellfound surfaces with detailed package estimates and micro-tech hubs")

with st.sidebar:
    st.header("🎯 Search Parameters")
    role = st.text_input("Target Role / Tech Stack", "Executive")
    location = st.text_input("Location / City", "Chennai")
    platform = st.radio("Platform Filter", ["All", "LinkedIn", "Naukri", "Indeed", "Foundit", "Wellfound"], horizontal=True)
    run_search = st.button("🚀 Find Fast-Approval Openings", type="primary", use_container_width=True)
    st.markdown("**Coverage:** Pan-India cities, remote, five public job portals, CTC, in-hand estimates, fixed/variable split, and joining bonus.")

if run_search or "job_data" not in st.session_state:
    with st.spinner(f"Harvesting opportunities for {role} in {location}..."):
        st.session_state.job_data = JobRadarEngine().find_fast_jobs(role, location, platform)

data = st.session_state.job_data
metrics = st.columns(4)
metrics[0].metric("Active Opportunities", data["total_found"], data["platform_filter"])
metrics[1].metric("Fast Approval (<24h)", data["fast_approval_count"])
metrics[2].metric(f"Top Hub ({data['resolved_city']})", data["top_hiring_area"])
if HAS_PDF:
    with metrics[3]:
        pdf = PDFReportGenerator().generate_job_radar_pdf(data)
        st.download_button("📄 Download Job Dossier", pdf, f"{data['role'].replace(' ', '_')}_job_dossier.pdf", "application/pdf", use_container_width=True)

st.subheader(f"📍 Area-Wise Hiring Density: {data['location'].title()} ({data['resolved_city']})")
areas = pd.DataFrame([{"Micro-Tech Hub": hub, "Active Openings": count} for hub, count in data["area_distribution"].items()])
st.dataframe(areas, use_container_width=True, hide_index=True)

st.subheader("⚡ Fast-Approval Opportunities with Package Forensics")
if data["jobs"]:
    jobs = pd.DataFrame(data["jobs"])
    columns = ["title", "company", "platform", "location", "area_hub", "velocity_score", "speed_badge", "ctc_display", "monthly_take_home", "fixed_split", "variable_split", "joining_bonus", "experience", "posted_time", "url"]
    st.dataframe(jobs[columns], use_container_width=True, hide_index=True, column_config={"url": st.column_config.LinkColumn("Apply")})
else:
    st.info("No matching openings found. Try All platforms or broaden the role.")

st.subheader("💬 Direct Recruiter Outreach Accelerator")
pitch = data["outreach_pitch"]
st.info(f"Best application timing: {pitch['best_time_to_apply']}")
left, right = st.columns(2)
with left:
    st.markdown("#### LinkedIn InMail / Recruiter DM")
    st.code(pitch["linkedin_inmail"], language="text")
with right:
    st.markdown("#### Cold Application Email")
    st.code(pitch["cold_email"], language="text")
