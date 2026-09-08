import streamlit as st
import pandas as pd
from core.job_engine import JobRadarEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(
    page_title="JobRadar | All-India Fast Job & Package Intelligence",
    page_icon="💼",
    layout="wide"
)

# Custom Styling for Job Intelligence
st.markdown("""
<style>
    .job-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
        transition: border-color 0.2s;
    }
    .job-card:hover {
        border-color: #38bdf8;
    }
    .badge-fast {
        background: #15803d;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
    }
    .badge-linkedin {
        background: #0077b5;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-naukri {
        background: #0284c7;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-indeed {
        background: #2557a7;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-foundit {
        background: #6d28d9;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-wellfound {
        background: #dc2626;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .package-box {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 10px 0;
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: center;
    }
    .metric-box {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .pitch-box {
        background: #0f172a;
        border-left: 4px solid #38bdf8;
        padding: 14px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 13px;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

st.title("💼 JobRadar: All-India Fast Job & Package Intelligence")
st.caption("Pan-India Live Harvester • LinkedIn, Naukri, Indeed, Foundit & Wellfound • Granular In-Hand Take-Home CTC • Accurate Micro-Tech Hubs • Zero API Keys")

with st.sidebar:
    st.header("🎯 Search Parameters")
    role_input = st.text_input(
        "Target Role / Tech Stack:",
        value="Executive",
        placeholder="e.g. Executive, Python, React, Data Scientist, Sales Manager"
    )
    loc_input = st.text_input(
        "Location / City (All India):",
        value="Chennai",
        placeholder="e.g. Chennai, Bengaluru, Hyderabad, Pune, Mumbai, Delhi, Coimbatore, All India, Remote"
    )
    
    platform_choice = st.radio(
        "Platform Filter:",
        ["All", "LinkedIn", "Naukri", "Indeed", "Foundit", "Wellfound"],
        horizontal=True
    )
    
    run_btn = st.button("🚀 Find Fast-Approval Openings", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("""
    **Intelligence Coverage:**
    - 🇮🇳 **Whole-of-India:** Tier 1, Tier 2, Tier 3 tech clusters & Remote
    - 🌐 **5 Top Portals:** LinkedIn, Naukri, Indeed, Foundit, Wellfound
    - 💰 **Detailed Packages:** CTC, in-hand take-home, fixed/variable split, joining bonus
    - ⚡ **Fast Approval (<24h):** High recruiter review activity
    - 💬 **Outreach Engine:** Automated InMail & cold email pitches
    """)

if run_btn or "job_data" not in st.session_state:
    with st.spinner(f"Harvesting fast-approval opportunities for '{role_input}' in '{loc_input}' across top job portals..."):
        engine = JobRadarEngine()
        data = engine.find_fast_jobs(role_input, loc_input, platform_choice)
        st.session_state["job_data"] = data

if "job_data" in st.session_state:
    data = st.session_state["job_data"]
    
    # -------------------------------------------------------------
    # 1. TOP METRICS
    # -------------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Opportunities Found", data["total_found"], f"Filtered: {data['platform_filter']}")
    m2.metric("⚡ Fast-Track (<24h Approval)", data["fast_approval_count"], "Priority Interview Queue")
    m3.metric(f"📍 Top Hub ({data['resolved_city']})", data["top_hiring_area"].split("(")[0].strip())
    
    with m4:
        st.write("")
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_job_radar_pdf(data)
            if pdf_bytes:
                st.download_button(
                    "📄 Download Job Dossier PDF",
                    pdf_bytes,
                    file_name=f"{data['role'].replace(' ', '_')}_{data['location']}_Job_Dossier.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )

    st.markdown("---")

    # -------------------------------------------------------------
    # 2. ACCURATE AREA-WISE HIRING DENSITY FOR MATCHED CITY
    # -------------------------------------------------------------
    st.subheader(f"📍 Area-Wise Hiring Density: {data['location'].title()} ({data['resolved_city']} Tech Zones)")
    st.caption("Accurately categorized by regional tech corridors, SEZ business parks, and commercial hubs.")
    
    area_dist = data.get("area_distribution", {})
    if area_dist:
        # Render clean interactive table & cards
        df_areas = pd.DataFrame([
            {"Micro-Tech Hub": k, "Active Fast Openings": v, "Hiring Velocity": "⚡ Immediate Joiners Active"}
            for k, v in sorted(area_dist.items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(df_areas, use_container_width=True, hide_index=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # 3. HIGH-VELOCITY OPENINGS WITH DETAILED PACKAGES
    # -------------------------------------------------------------
    st.subheader(f"⚡ Fast-Approval Opportunities with Package Forensics")
    st.caption("Sorted by Response Velocity Score. Includes estimated in-hand take-home, fixed vs bonus split, and direct apply links.")

    jobs = data.get("jobs", [])
    if jobs:
        for j in jobs:
            plat = j['platform']
            if plat == 'LinkedIn': plat_badge = '<span class="badge-linkedin">LinkedIn</span>'
            elif plat == 'Naukri': plat_badge = '<span class="badge-naukri">Naukri</span>'
            elif plat == 'Indeed': plat_badge = '<span class="badge-indeed">Indeed</span>'
            elif plat == 'Foundit': plat_badge = '<span class="badge-foundit">Foundit</span>'
            else: plat_badge = '<span class="badge-wellfound">Wellfound</span>'

            tags_html = " ".join([f"<span style='background: #334155; color: #cbd5e1; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-right: 4px;'>{t}</span>" for t in j['tags']])
            
            st.markdown(f"""
            <div class="job-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin: 0 0 6px 0; color: #f8fafc;">
                            {j['title']} 
                            {plat_badge}
                        </h3>
                        <h4 style="margin: 0 0 8px 0; color: #38bdf8;">🏢 {j['company']} • <span style="color: #94a3b8; font-size: 14px;">📍 {j['location']}</span></h4>
                    </div>
                    <div style="text-align: right;">
                        <span class="badge-fast">{j['speed_badge']}</span>
                        <div style="font-size: 13px; color: #38bdf8; font-weight: bold; margin-top: 4px;">Velocity: {j['velocity_score']}/100</div>
                    </div>
                </div>
                
                <!-- Detailed Package Breakdown -->
                <div class="package-box">
                    <div>💰 <b>Total CTC:</b> <span style="color: #4ade80; font-weight: bold; font-size: 15px;">{j['ctc_display']}</span></div>
                    <div>💵 <b>In-Hand Take-Home:</b> <span style="color: #38bdf8;">{j['monthly_take_home']}</span></div>
                    <div>📊 <b>Split:</b> {j['fixed_split']} + {j['variable_split']}</div>
                    <div>🎁 <b>Bonus:</b> {j['joining_bonus']}</div>
                    <div>💼 <b>Experience:</b> {j['experience']}</div>
                </div>

                <div style="margin: 8px 0;">{tags_html}</div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
                    <span style="font-size: 12px; color: #94a3b8;">🕒 Posted: <b>{j['posted_time']}</b> • Micro-Hub: <b>{j['area_hub']}</b></span>
                    <a href="{j['url']}" target="_blank" style="background: #0284c7; color: white; padding: 7px 16px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold;">
                        🚀 Apply on {j['platform']}
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No matching openings found. Try selecting 'All' platforms or broadening the search terms.")

    st.markdown("---")

    # -------------------------------------------------------------
    # 4. RECRUITER OUTREACH ACCELERATOR
    # -------------------------------------------------------------
    st.subheader("💬 Direct Recruiter Outreach Accelerator")
    st.caption("Send these high-converting personalized messages to hiring managers to bypass the resume black hole.")

    pitch = data.get("outreach_pitch", {})
    st.info(f"💡 **Optimal Application Timing:** {pitch.get('best_time_to_apply', 'Morning 9-11 AM IST')}")

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown("#### 📱 LinkedIn InMail / Recruiter Connection DM")
        st.markdown(f'<div class="pitch-box">{pitch.get("linkedin_inmail", "")}</div>', unsafe_allow_html=True)

    with t_col2:
        st.markdown("#### ✉️ Executive Cold Application Email")
        st.markdown(f'<div class="pitch-box">{pitch.get("cold_email", "")}</div>', unsafe_allow_html=True)
