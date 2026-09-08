import urllib.parse
import pandas as pd
import streamlit as st
from core.company_engine import CompanyIntelEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="CompanyIntel | Corporate OSINT Dossier", page_icon="💼", layout="wide")

st.title("💼 CompanyIntel: Full-Spectrum Corporate & Enterprise OSINT Suite")
st.caption("360° public-surface intelligence: Workplace drama, employee rumors, M&A acquisitions, bonus news, legal cases, profit & loss financials, cafeteria perks, and employee survival playbook.")

# =====================================================================
# SIDEBAR CONTROLS & QUICK TARGET CHIPS
# =====================================================================
POPULAR_TARGETS = ["Nvidia", "Google", "Microsoft", "OpenAI", "Tesla", "TCS", "Zomato", "Stripe"]

with st.sidebar:
    st.header("🎯 Target Enterprise")
    quick_choice = st.selectbox("Quick-Select Popular Companies:", POPULAR_TARGETS, index=0)
    c_target = st.text_input("Or Enter Any Company Name:", value="", placeholder="e.g. Apple, Amazon, Infosys, Swiggy, Netflix")
    active_company = c_target.strip() if c_target.strip() else quick_choice

    st.markdown("---")
    st.markdown(
        """
        **🛰️ OSINT Intelligence Scope:**
        - 🔥 Drama, Gossip & Rumors (Reddit/Blind)
        - 📊 Financial Health & P&L (Revenue/Margin)
        - 🤝 Recent Acquisitions & M&A Deals
        - 🎁 Bonus News, Hikes & Appraisals
        - ⚖️ Legal Cases & Antitrust Probes
        - 🛡️ Employee Survival Playbook (DNA/PIP/Notice)
        - 🍕 Workplace Environment, Food & Perks
        - 💰 Role-by-Role Salaries (USD & INR)
        - 👔 LinkedIn HR & Recruiter Radar
        - 🎯 Live Jobs & Multi-Portal Radar
        - 📰 Breaking News & Public Press Wire
        - 🏛️ Verified Corporate Profile & Factsheet
        """
    )

    run_btn = st.button("🚀 Retrieve Full OSINT Dossier", type="primary", use_container_width=True)

# Support trigger from quick launch buttons
if "trigger_company" in st.session_state and st.session_state["trigger_company"]:
    active_company = st.session_state["trigger_company"]
    st.session_state["trigger_company"] = None
    run_btn = True

# =====================================================================
# DATA RETRIEVAL & CACHING
# =====================================================================
if run_btn or "company_data" not in st.session_state or st.session_state.get("active_company_name") != active_company:
    with st.spinner(f"Running surface-web OSINT sweeps on '{active_company}' (Wikipedia, Reddit, Blind, LinkedIn, RSS News)..."):
        engine = CompanyIntelEngine()
        data = engine.get_company_dossier(active_company)
        st.session_state["company_data"] = data
        st.session_state["active_company_name"] = active_company

# =====================================================================
# MAIN DOSSIER INTERFACE
# =====================================================================
if "company_data" in st.session_state:
    data = st.session_state["company_data"]
    comp_title = data.get("title", data.get("company", "Enterprise"))
    drama = data.get("drama_radar", {})
    jobs = data.get("jobs_radar", {})
    fin = data.get("financials", {})
    bonuses = data.get("bonuses", {})
    survival = data.get("survival_briefing", {})
    acquisitions = data.get("acquisitions", [])
    legal_cases = data.get("legal_cases", [])
    deep_news = data.get("deep_news", [])

    # -----------------------------------------------------------------
    # HEADER: ENTITY IDENTITY & DIGITAL FOOTPRINT
    # -----------------------------------------------------------------
    h_col1, h_col2 = st.columns([3, 1])

    with h_col1:
        st.markdown(f"## 🏢 {comp_title}")
        st.caption(f"**Industry:** `{data.get('industry', 'Technology')}` • **Headquarters:** `{data.get('headquarters', 'Global')}` • **Headcount:** `{data.get('employees', '10,000+')}` • **Stock:** `{data.get('stock', 'N/A')}`")

        # Verified Footprint Quick Action Links
        footprint_html = f"""
        <div style='margin-top: 6px; margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 6px;'>
            <a href='{data.get("website")}' target='_blank' style='text-decoration: none;'><button style='background-color:#0284c7; color:white; border:none; border-radius:4px; padding:5px 11px; cursor:pointer; font-size:12px; font-weight:500;'>🌐 Official Website</button></a>
            <a href='{data.get("linkedin")}' target='_blank' style='text-decoration: none;'><button style='background-color:#0077b5; color:white; border:none; border-radius:4px; padding:5px 11px; cursor:pointer; font-size:12px; font-weight:500;'>💼 LinkedIn Page</button></a>
            <a href='{data.get("careers")}' target='_blank' style='text-decoration: none;'><button style='background-color:#10b981; color:white; border:none; border-radius:4px; padding:5px 11px; cursor:pointer; font-size:12px; font-weight:500;'>🚀 Careers Portal</button></a>
            <a href='{data.get("glassdoor_url")}' target='_blank' style='text-decoration: none;'><button style='background-color:#0caa41; color:white; border:none; border-radius:4px; padding:5px 11px; cursor:pointer; font-size:12px; font-weight:500;'>🏢 Glassdoor</button></a>
            <a href='{data.get("blind_url")}' target='_blank' style='text-decoration: none;'><button style='background-color:#2b2d42; color:white; border:none; border-radius:4px; padding:5px 11px; cursor:pointer; font-size:12px; font-weight:500;'>💬 Blind Reviews</button></a>
            <a href='{data.get("reddit_url")}' target='_blank' style='text-decoration: none;'><button style='background-color:#ff4500; color:white; border:none; border-radius:4px; padding:5px 11px; cursor:pointer; font-size:12px; font-weight:500;'>👽 Reddit Discussions</button></a>
        </div>
        """
        st.markdown(footprint_html, unsafe_allow_html=True)

    with h_col2:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_company_pdf(data.get("company", "Company"), data)
            if pdf_bytes:
                st.download_button(
                    "📄 Export Full OSINT PDF",
                    pdf_bytes,
                    f"{data.get('company')}_OSINT_Corporate_Dossier.pdf",
                    "application/pdf",
                    type="primary",
                    use_container_width=True
                )
        else:
            st.caption("PDF Report Ready")

    # Top KPI Metrics Row 1: Culture, Food, Drama
    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Work-Life Balance", f"{data.get('wlb_score', 4.0)} / 5.0", "Employee Consensus")
    with k2:
        st.metric("Learning & Velocity", f"{data.get('learning_score', 4.5)} / 5.0", "Growth Environment")
    with k3:
        st.metric("Food & Cafeteria", f"{data.get('food_score', 4.5)} / 5.0", "Dining & Amenities")
    with k4:
        st.metric("Public Controversy Index", f"{drama.get('controversy_score', 35)}/100", drama.get('risk_badge', 'STABLE'))

    # Top KPI Metrics Row 2: Financials & Survival Indicators
    k5, k6, k7, k8 = st.columns(4)
    with k5:
        st.metric("Annual Revenue", str(fin.get("annual_revenue", "N/A")), fin.get("yoy_growth", "Stable"))
    with k6:
        st.metric("Net Profit Margin", str(fin.get("net_profit", "Profitable")), fin.get("health_status", "Solid"))
    with k7:
        st.metric("Layoff Safety Rating", str(survival.get("pip_layoff_safety", "8.0/10")), "Job Security Score")
    with k8:
        st.metric("Avg Merit Hike", str(bonuses.get("hike_avg", "8% - 12%")), bonuses.get("multiplier", "Target Multiplier"))

    st.markdown("---")

    # =================================================================
    # 12 DEDICATED OSINT TABS (COMPLETE EMPLOYEE INTELLIGENCE)
    # =================================================================
    (
        tab_drama,
        tab_finance,
        tab_acquisitions,
        tab_bonuses,
        tab_legal,
        tab_survival,
        tab_culture,
        tab_salary,
        tab_hr,
        tab_jobs,
        tab_news,
        tab_wiki
    ) = st.tabs([
        "🔥 Drama & Rumors",
        "📊 Profit & Loss (P&L)",
        "🤝 Recent Acquisitions",
        "🎁 Bonus News & Hikes",
        "⚖️ Legal Cases & Probes",
        "🛡️ Employee Survival Handbook",
        "🍕 Workplace, Food & Perks",
        "💰 Salary & Equity Forensics",
        "👔 HR & Recruiter Radar",
        "🎯 Live Jobs & Radar",
        "📰 Breaking News Wire",
        "🏛️ Corporate Profile"
    ])

    # -----------------------------------------------------------------
    # TAB 1: DRAMA, GOSSIP & RUMORS
    # -----------------------------------------------------------------
    with tab_drama:
        st.markdown("### 🔥 Real-Time Controversy, Gossip & Rumor Wire")
        st.caption("Aggregated from Reddit (r/cscareerquestions, r/technology, r/antiwork), Blind, and financial investigative reports.")

        # Drama Risk Status Box
        risk_badge = drama.get("risk_badge", "STABLE")
        risk_score = drama.get("controversy_score", 30)

        if risk_score >= 65:
            st.error(f"### {risk_badge}\nHigh volume of public discussions regarding restructuring, internal friction, or policy changes detected.")
        elif risk_score >= 40:
            st.warning(f"### {risk_badge}\nModerate conversational buzz regarding RTO mandates, compensation calibration, or project shifts.")
        else:
            st.success(f"### {risk_badge}\nLow controversy detected across public feeds; stable workplace sentiment.")

        st.markdown("#### 📢 Monitored Discussion Threads & News Drops")
        items = drama.get("items", [])
        if items:
            for item in items:
                with st.expander(f"{item.get('tag', '📢')} | {item.get('headline')}", expanded=True):
                    st.write(f"**Source:** `{item.get('source')}` • **Date / Time:** `{item.get('pub_date')}`")
                    st.markdown(f"[🔗 Open Public Discussion Thread / Article]({item.get('link')})")
        else:
            st.info("No significant negative controversy threads detected in the current 30-day window.")

        st.markdown("---")
        st.markdown("#### 🕵️ Anonymous Employee Channels")
        an_col1, an_col2 = st.columns(2)
        with an_col1:
            st.markdown(
                f"""
                - [💬 Open Verified Blind Threads for {active_company}]({data.get('blind_url')})
                - [👽 Search Reddit Career & Layoff Discussions]({data.get('reddit_url')})
                """
            )
        with an_col2:
            st.markdown(
                f"""
                - [🏢 Glassdoor Anonymous CEO Approval & Review Scorecard]({data.get('glassdoor_url')})
                - [🔍 Google News Dork: Restructuring & Leaks](https://www.google.com/search?q={urllib.parse.quote(active_company)}+layoffs+restructuring+memo)
                """
            )

    # -----------------------------------------------------------------
    # TAB 2: FINANCIAL HEALTH, PROFIT & LOSS (P&L)
    # -----------------------------------------------------------------
    with tab_finance:
        st.markdown("### 📊 Financial Health, Profit & Loss (P&L) Forensics")
        st.caption("What every employee must know about the company's financial runway, revenue generation, and balance sheet safety.")

        f_c1, f_c2 = st.columns(2)
        with f_c1:
            st.markdown("#### 💵 Revenue & Earnings Fundamentals")
            st.info(f"**Annual Revenue:** `{fin.get('annual_revenue', 'N/A')}`")
            st.success(f"**Net Profit & Margin:** `{fin.get('net_profit', 'N/A')}`")
            st.write(f"• **Year-Over-Year Growth:** `{fin.get('yoy_growth', 'N/A')}`")
            st.write(f"• **Cash Reserves & Liquid Assets:** `{fin.get('cash_reserves', 'N/A')}`")

        with f_c2:
            st.markdown("#### 🛡️ Balance Sheet Health & Layoff Safety")
            st.write(f"**Overall Health Rating:** `{fin.get('health_status', 'Healthy')}`")
            st.warning(f"**Runway & Job Security Verdict:**\n\n{fin.get('runway_verdict', 'Stable commercial operations with low immediate layoff risk.')}")

        st.markdown("---")
        st.markdown("#### 📈 Public Financial Intelligence Dorks")
        p_c1, p_c2, p_c3 = st.columns(3)
        with p_c1:
            st.markdown(f"[📈 SEC EDGAR / Annual 10-K Filings](https://www.sec.gov/edgar/searchedgar/companysearch?companyName={urllib.parse.quote(active_company)})")
        with p_c2:
            st.markdown(f"[📊 Yahoo Finance Financial Statements](https://finance.yahoo.com/lookup?s={urllib.parse.quote(active_company)})")
        with p_c3:
            st.markdown(f"[📰 Google Finance Live Stock & Earnings](https://www.google.com/finance/quote/{urllib.parse.quote(active_company)})")

    # -----------------------------------------------------------------
    # TAB 3: RECENT ACQUISITIONS & M&A DEALS
    # -----------------------------------------------------------------
    with tab_acquisitions:
        st.markdown("### 🤝 Recent Acquisitions, M&A Deals & Tech Absorption")
        st.caption("Strategic corporate buyouts: What companies were acquired, deal valuations, and how technologies were absorbed.")

        if acquisitions:
            for acq in acquisitions:
                with st.container():
                    a1, a2 = st.columns([3, 1])
                    with a1:
                        st.markdown(f"#### 🎯 {acq.get('company')} ({acq.get('year', 'Recent')})")
                        st.write(f"**Strategic Rationale:** {acq.get('rationale')}")
                        st.write(f"**Current Status & Tech Absorption:** `{acq.get('status')}`")
                    with a2:
                        st.metric("Deal Valuation", acq.get("deal_value", "Undisclosed"))
                        st.markdown(f"<a href='https://www.google.com/search?q={urllib.parse.quote(active_company)}+acquired+{urllib.parse.quote(acq.get('company'))}' target='_blank'><button style='background-color:#0284c7; color:white; border:none; border-radius:4px; padding:6px 12px; cursor:pointer; width:100%; margin-top:8px;'>🔍 Deal Coverage</button></a>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info(f"No major public M&A acquisitions recorded recently for {active_company}.")

        st.markdown("#### 💡 Why This Matters to Employees")
        st.markdown(
            """
            - **Acqui-hires & Leadership Reshuffles:** Acquired startup founders often take over internal divisions.
            - **Tech Stack Harmonization:** Indicates which technologies (e.g. AI frameworks, infrastructure engines) the company is investing in.
            - **Redundancy Risks:** Overlapping duplicate departments (e.g. general corporate sales, HR) are often consolidated post-deal.
            """
        )

    # -----------------------------------------------------------------
    # TAB 4: BONUS NEWS, HIKES & APPRAISAL CALIBRATION
    # -----------------------------------------------------------------
    with tab_bonuses:
        st.markdown("### 🎁 Bonus Payouts, Annual Hikes & Appraisal Calibration")
        st.caption("Forensic breakdown of how bonuses are calculated, merit hike distributions, and actual employee payout reports.")

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            st.markdown("#### 🎯 Compensation Multipliers")
            st.metric("Target Bonus Multiplier", bonuses.get("multiplier", "100% Target"))
            st.metric("Average Base Increment", bonuses.get("hike_avg", "6% - 10%"))
            st.info(f"**Appraisal Timing:** {bonuses.get('appraisal_cycle', 'Annual cycle')}")

        with b_c2:
            st.markdown("#### ⚖️ Rating Curve & Calibration Strategy")
            st.warning(f"**Curve Structure:** {bonuses.get('rating_curve', 'Standard distribution curve based on departmental deliverables.')}")
            st.markdown(
                """
                **💡 Key Tactics to Maximize Your Bonus & Hike:**
                - Align deliverables directly with executive OKRs before the calibration freeze.
                - Collect written peer praise and multi-stakeholder impact metrics early.
                - For equity refreshes, highlight critical tribal knowledge and retention flight-risk factors.
                """
            )

        st.markdown("---")
        st.markdown("#### 📢 Monitored Bonus News & Internal Payout Drops")
        b_news = bonuses.get("news", [])
        if b_news:
            for bn in b_news:
                st.write(f"• 💰 **{bn}**")
        else:
            st.write(f"• 💰 Annual merit increments and corporate performance pool bonuses are distributed according to verified divisional targets.")

    # -----------------------------------------------------------------
    # TAB 5: LEGAL CASES, LAWSUITS & REGULATORY PROBES
    # -----------------------------------------------------------------
    with tab_legal:
        st.markdown("### ⚖️ Legal Cases, Antitrust Probes & Regulatory Actions")
        st.caption("Active DOJ, FTC, EU Commission, CCI, and intellectual property litigation impacting company operations.")

        if legal_cases:
            for case in legal_cases:
                with st.expander(f"⚖️ {case.get('case_title')}", expanded=True):
                    st.write(f"**Jurisdiction / Regulatory Body:** `{case.get('jurisdiction')}`")
                    st.write(f"**Key Allegation / Focus:** {case.get('allegation')}")
                    st.write(f"**Current Legal Status:** `{case.get('status')}`")
                    st.error(f"**Employee Impact & Operational Risk:** {case.get('employee_impact')}")
                    st.markdown(f"[🔍 Search Ongoing Legal Docket](https://www.google.com/search?q={urllib.parse.quote(case.get('case_title'))})")
        else:
            st.info(f"No high-profile existential litigation or regulatory antitrust probes detected for {active_company}.")

        st.markdown("---")
        st.markdown("#### 🛡️ Compliance Hygiene Checklist for Employees")
        st.markdown(
            """
            - **Document Retention Notices:** Never delete Slack/Teams messages or emails if under an active legal hold.
            - **IP Cleanliness:** Never import third-party code or proprietary material from previous employers into internal repositories.
            - **Antitrust Awareness:** Avoid participating in unauthorized informal industry wage or non-poach agreements.
            """
        )

    # -----------------------------------------------------------------
    # TAB 6: EMPLOYEE SURVIVAL HANDBOOK
    # -----------------------------------------------------------------
    with tab_survival:
        st.markdown("### 🛡️ Employee Survival Handbook & Internal Playbook")
        st.caption("The unwritten rules: Organizational DNA, promotion secrets, PIP & layoff vulnerability, moonlighting policies, and notice periods.")

        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown("#### 🧬 Organizational DNA & Work Ethic")
            st.info(survival.get("org_dna", "Engineering-led, metrics-driven meritocracy."))

            st.markdown("#### 🚀 Promotion Secrets & Career Velocity")
            st.success(survival.get("promotion_secrets", "Demonstrate business impact on core metrics and maintain high cross-functional visibility."))

            st.markdown("#### 🛡️ PIP & Layoff Vulnerability Assessment")
            st.warning(f"**Safety Score:** `{survival.get('pip_layoff_safety', '7.5/10')}`\n\nSeek continuous 1-on-1 alignment with your reporting manager to safeguard against surprise performance plans.")

        with s_col2:
            st.markdown("#### 🌙 Moonlighting & Side-Hustle Policy")
            st.write(f"**Current Rule:** {survival.get('moonlighting_policy', 'Strict prohibition on competing ventures; open source allowed with legal approval.')}")

            st.markdown("#### ⏳ Notice Period & Offboarding Rules")
            st.write(f"**Notice Required:** `{survival.get('notice_period', '30 to 90 Days depending on region and contract.')}`")

            st.markdown("#### 🧰 The New Joiner First 90 Days Checklist")
            st.markdown(
                """
                - **Day 1-30:** Map out the informal decision-makers and schedule 15-min coffee chats.
                - **Day 31-60:** Ship a small, highly visible bug fix or feature to production to test deployment pipelines.
                - **Day 61-90:** Establish documented OKRs with your manager with explicit criteria for 'Exceeds Expectations'.
                """
            )

    # -----------------------------------------------------------------
    # TAB 7: WORKPLACE, FOOD & CULTURE
    # -----------------------------------------------------------------
    with tab_culture:
        st.markdown("### 🍕 Workplace Environment, Food & Perks Intelligence")

        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st.markdown("#### 🏢 Return-to-Office & Hybrid Policy")
            st.info(f"**Current Enforcement:** {data.get('rto_policy', 'Hybrid Policy')}")

            st.markdown("#### 🍲 Cafeteria, Dining & Food Perks")
            st.write(data.get("food_perks", "Subsidized corporate dining options available."))

            st.markdown("#### 📚 Learning, Mentorship & Tech Horizon")
            st.write(data.get("learning_perks", "Structured internal training and conference sponsorships."))

        with c_col2:
            st.markdown("#### 🎁 Comprehensive Employee Perks Checklist")
            for perk in data.get("perks_list", []):
                st.write(f"• ✅ {perk}")

        st.markdown("---")
        st.markdown("#### ⚖️ Employee Consensus: Pros vs Cons")
        pro_col, con_col = st.columns(2)
        with pro_col:
            st.markdown("##### 🟢 Major Verified Pros")
            for pro in data.get("pros", []):
                st.success(f"• {pro}")
        with con_col:
            st.markdown("##### 🔴 Major Verified Cons")
            for con in data.get("cons", []):
                st.error(f"• {con}")

    # -----------------------------------------------------------------
    # TAB 8: SALARY & COMPENSATION FORENSICS
    # -----------------------------------------------------------------
    with tab_salary:
        st.markdown("### 💰 Compensation, Equity & Salary Forensics")
        st.caption(f"Estimated compensation bands benchmarked against `{data.get('salary_tier', 'Tier 1 Tech')}` market compensation levels.")

        salaries = data.get("salaries", [])
        if salaries:
            df_sal = pd.DataFrame(salaries)
            df_sal.columns = ["Role & Level", "🇺🇸 US Market Range", "🇮🇳 India Market Range", "Stock / Bonus Structure"]
            st.dataframe(df_sal, use_container_width=True, hide_index=True)

        st.markdown("---")
        sal_c1, sal_c2 = st.columns(2)
        with sal_c1:
            st.markdown("#### 📈 Typical Equity (RSU) Vesting Schedule")
            st.markdown(
                """
                - **Standard Vesting:** 4-Year Schedule with 25% vest per year, or monthly/quarterly vesting after 1-year cliff.
                - **Annual Refresher Grants:** High performers typically receive 15%-30% RSU refreshers annually.
                - **ESPP:** 15% discount on fair market value (FMV) via 6-month lookback periods where offered.
                """
            )
        with sal_c2:
            st.markdown("#### 🔍 Salary Research Dork Links")
            st.markdown(
                f"""
                - [🔗 View Verified Salaries on Levels.fyi](https://www.levels.fyi/companies/{urllib.parse.quote(active_company.lower())}/salaries)
                - [🔗 View India Salaries on AmbitionBox](https://www.ambitionbox.com/salaries/{urllib.parse.quote(active_company.lower())}-salaries)
                - [🔗 View Glassdoor Total Compensation Reports](https://www.glassdoor.com/Salary/{urllib.parse.quote(active_company)}-Salaries-E.htm)
                """
            )

    # -----------------------------------------------------------------
    # TAB 9: HR MANAGERS & RECRUITERS
    # -----------------------------------------------------------------
    with tab_hr:
        st.markdown("### 👔 HR & Talent Acquisition Leadership Directory")
        st.caption("Targeted LinkedIn OSINT dorks for identifying hiring managers, technical recruiters, and talent decision-makers.")

        hr_list = data.get("hr_directory", [])
        for hr in hr_list:
            with st.container():
                c_role, c_act = st.columns([3, 1])
                with c_role:
                    st.markdown(f"#### {hr.get('role_type')}")
                    st.write(f"**Focus Area:** {hr.get('focus')} • **Location:** `{hr.get('location')}`")
                with c_act:
                    st.markdown(f"<a href='{hr.get('dork_url')}' target='_blank'><button style='background-color:#0077b5; color:white; border:none; border-radius:4px; padding:8px 14px; cursor:pointer; width:100%; margin-top:10px;'>🔍 Search Profiles on LinkedIn</button></a>", unsafe_allow_html=True)
                st.markdown("---")

        st.markdown("#### 📨 1-Click HR & Recruiter Cold Pitch Generator")
        with st.expander("📝 View & Copy Tailored Recruiter Outreach Pitch", expanded=False):
            st.code(data.get("pitch_template", ""), language="markdown")

    # -----------------------------------------------------------------
    # TAB 10: LIVE JOBS & HIRING RADAR
    # -----------------------------------------------------------------
    with tab_jobs:
        st.markdown("### 🎯 Live Jobs & Hiring Channels")
        st.caption("Active hiring demand corridors and 1-click external portal searches.")

        st.markdown("#### ⚡ 1-Click Multi-Portal Job Dorks")
        j_c1, j_c2, j_c3, j_c4, j_c5 = st.columns(5)
        with j_c1:
            st.markdown(f"<a href='{jobs.get('linkedin_jobs')}' target='_blank'><button style='background-color:#0077b5; color:white; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; width:100%; font-weight:500;'>💼 LinkedIn Jobs</button></a>", unsafe_allow_html=True)
        with j_c2:
            st.markdown(f"<a href='{jobs.get('google_jobs')}' target='_blank'><button style='background-color:#0284c7; color:white; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; width:100%; font-weight:500;'>🔍 Google Careers</button></a>", unsafe_allow_html=True)
        with j_c3:
            st.markdown(f"<a href='{jobs.get('indeed_jobs')}' target='_blank'><button style='background-color:#2557a7; color:white; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; width:100%; font-weight:500;'>📄 Indeed Jobs</button></a>", unsafe_allow_html=True)
        with j_c4:
            st.markdown(f"<a href='{jobs.get('naukri_jobs')}' target='_blank'><button style='background-color:#275df5; color:white; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; width:100%; font-weight:500;'>🇮🇳 Naukri India</button></a>", unsafe_allow_html=True)
        with j_c5:
            st.markdown(f"<a href='{jobs.get('wellfound_jobs')}' target='_blank'><button style='background-color:#ff6154; color:white; border:none; border-radius:4px; padding:8px 12px; cursor:pointer; width:100%; font-weight:500;'>🚀 Wellfound</button></a>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📍 In-Demand Department Openings")
        for opening in jobs.get("hot_openings", []):
            st.markdown(
                f"""
                - **{opening.get('title')}**
                  - Department: `{opening.get('dept')}` • Location: `{opening.get('loc')}` • Experience: `{opening.get('exp')}`
                """
            )

    # -----------------------------------------------------------------
    # TAB 11: BREAKING NEWS & PUBLIC PRESS WIRE
    # -----------------------------------------------------------------
    with tab_news:
        st.markdown("### 📰 Breaking News & Corporate Press Wire")
        st.caption(f"Real-time press releases, financial news, and executive announcements regarding {active_company}.")

        if deep_news:
            for n in deep_news:
                with st.expander(f"📰 {n.get('title')}", expanded=True):
                    st.write(f"**Publisher / Wire:** `{n.get('source')}` • **Date:** `{n.get('pub_date')}`")
                    st.markdown(f"[🔗 Read Full Article Online]({n.get('link')})")
        else:
            st.info(f"No breaking news articles returned in the current RSS sweep for {active_company}.")

    # -----------------------------------------------------------------
    # TAB 12: CORPORATE ENTITY PROFILE
    # -----------------------------------------------------------------
    with tab_wiki:
        st.markdown("### 🏛️ Verified Corporate Profile & Encyclopedia Record")

        w_col1, w_col2 = st.columns([3, 1])
        with w_col1:
            st.write(data.get("extract", "No verified Wikipedia overview available."))
            if data.get("page_url"):
                st.markdown(f"🔗 [Read Full Verified Entity Wikipedia Documentation]({data['page_url']})")

        with w_col2:
            st.markdown("#### 📋 Entity Quick Facts")
            st.write(f"• **CEO:** {data.get('ceo', 'N/A')}")
            st.write(f"• **Founded:** {data.get('founded', 'N/A')}")
            st.write(f"• **Headquarters:** {data.get('headquarters', 'N/A')}")
            st.write(f"• **Stock Ticker:** `{data.get('stock', 'N/A')}`")
            st.write(f"• **Employees:** `{data.get('employees', 'N/A')}`")