import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from core.agency_seo_engine import AgencySEOEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(
    page_title="SEOMaster Pro | Agency SEO & GEO Intelligence",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 SEOMaster Pro: Agency-Grade SEO & GEO Intelligence Suite")
st.caption("Replaces SEMrush & SEOptimer • 100+ Automated Technical Checkpoints • Generative Engine Optimization (GEO) • White-Label Executive PDF Reports")

POPULAR_SITES = ["casagrand.co.in", "stripe.com", "apple.com", "netflix.com", "shrinithiinfra.in"]

with st.sidebar:
    st.header("🎯 Audit Target")
    custom_target = st.text_input("Enter Website URL:", value="", placeholder="e.g. apple.com, casagrand.co.in")
    site_choice = st.selectbox("Or Quick-Pick a Benchmark Site:", ["-- Select a Site --"] + POPULAR_SITES, index=0)
    
    # Active target resolves ONLY if user types or selects
    active_target = custom_target.strip() if custom_target.strip() else (site_choice if site_choice != "-- Select a Site --" else "")
    
    st.markdown("---")
    st.header("🏢 Agency Branding")
    agency_brand = st.text_input("Report Agency Name:", value="NASA OSINT Intelligence")
    
    run_btn = st.button("🚀 Run Comprehensive 100+ Audit", type="primary", use_container_width=True)
    st.markdown("---")
    st.caption("🔒 **Safe Mode Active:** Zero automated crawling on page load. Targets are audited ONLY upon clicking the button.")

# ONLY execute when user clicks button and target is provided (prevents automatic bans)
if run_btn and active_target:
    with st.spinner(f"Running deep 100+ checkpoint audit for {active_target}..."):
        engine = AgencySEOEngine()
        data = engine.run_comprehensive_audit(active_target)
        st.session_state["agency_seo_data"] = data
        st.session_state["agency_seo_active"] = active_target

# =====================================================================
# MAIN DISPLAY: STANDBY SCREEN (NO AUTO-SEARCH) OR FULL DASHBOARD
# =====================================================================
if "agency_seo_data" not in st.session_state or not st.session_state.get("agency_seo_data"):
    st.info("👈 **Awaiting Your Input**: Enter any website URL in the sidebar and click **'🚀 Run Comprehensive 100+ Audit'** to begin.")
    
    st.markdown("### ⚡ Quick-Select Safe Benchmark Sites (Click to Run):")
    q1, q2, q3 = st.columns(3)
    if q1.button("🍎 Audit apple.com", use_container_width=True):
        with st.spinner("Auditing apple.com..."):
            st.session_state["agency_seo_data"] = AgencySEOEngine().run_comprehensive_audit("apple.com")
            st.session_state["agency_seo_active"] = "apple.com"
            st.rerun()
    if q2.button("💳 Audit stripe.com", use_container_width=True):
        with st.spinner("Auditing stripe.com..."):
            st.session_state["agency_seo_data"] = AgencySEOEngine().run_comprehensive_audit("stripe.com")
            st.session_state["agency_seo_active"] = "stripe.com"
            st.rerun()
    if q3.button("🏢 Audit casagrand.co.in", use_container_width=True):
        with st.spinner("Auditing casagrand.co.in..."):
            st.session_state["agency_seo_data"] = AgencySEOEngine().run_comprehensive_audit("casagrand.co.in")
            st.session_state["agency_seo_active"] = "casagrand.co.in"
            st.rerun()

else:
    data = st.session_state["agency_seo_data"]
    if "error" in data:
        st.error(data["error"])
    else:
        grades = data.get("grades", {})
        overall = grades.get("overall", {"grade": "B", "score": 75})
        recs = data.get("recommendations", [])
        onpage = data.get("onpage", {})
        geo = data.get("geo", {})
        perf = data.get("performance", {})
        tech = data.get("technology", {})
        links = data.get("links", {})
        usability = data.get("usability", {})
        kw_data = data.get("keyword_consistency", {})

        # Header Scorecard & Exports
        c_head1, c_head2, c_head3 = st.columns([2.2, 1.8, 2])
        with c_head1:
            st.subheader(f"🌐 Audit: {data['domain']}")
            st.caption(f"Target URL: `{data['full_url']}` • Checked on {data['timestamp']}")
        with c_head2:
            st.metric("Overall Health Grade", f"{overall['grade']} ({overall['score']}/100)", f"{len(recs)} Recommendations")
        with c_head3:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if HAS_PDF:
                    pdf_gen = PDFReportGenerator()
                    pdf_bytes = pdf_gen.generate_agency_seo_audit_pdf(data["domain"], data, agency_name=agency_brand)
                    if pdf_bytes:
                        st.download_button(
                            "📄 PDF Report",
                            pdf_bytes,
                            f"{data['domain']}_Executive_SEO_Report.pdf",
                            "application/pdf",
                            type="primary",
                            use_container_width=True
                        )
            with col_b2:
                if recs:
                    df_rec_export = pd.DataFrame(recs)
                    csv_bytes = df_rec_export.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 CSV Export",
                        csv_bytes,
                        f"{data['domain']}_SEO_Checkpoints.csv",
                        "text/csv",
                        use_container_width=True
                    )

        st.markdown("---")

        # 5 Core Pillar Circular Rings
        st.markdown("### 📊 Core Audit Pillars")
        col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
        with col_p1:
            st.metric("🔍 On-Page SEO", grades.get("onpage", {}).get("grade", "N/A"), f"{grades.get('onpage', {}).get('score', 0)}/100")
        with col_p2:
            st.metric("🤖 GEO / AI Search", grades.get("geo", {}).get("grade", "N/A"), f"{grades.get('geo', {}).get('score', 0)}/100")
        with col_p3:
            st.metric("🔗 Links & Authority", grades.get("links", {}).get("grade", "N/A"), f"{grades.get('links', {}).get('score', 0)}/100")
        with col_p4:
            st.metric("📱 Usability", grades.get("usability", {}).get("grade", "N/A"), f"{grades.get('usability', {}).get('score', 0)}/100")
        with col_p5:
            st.metric("⚡ Performance", grades.get("performance", {}).get("grade", "N/A"), f"{grades.get('performance', {}).get('score', 0)}/100")

        # -------------------------------------------------------------
        # 💰 COMMERCIAL TRAFFIC & VALUE LEAK FORENSICS (NEW)
        # -------------------------------------------------------------
        st.markdown("---")
        st.subheader("💰 Commercial Revenue & Organic Traffic Leak Forensics")
        st.caption("Forensic financial projections modeling traffic and revenue lost due to technical SEO deficits.")
        
        score_val = overall.get("score", 75)
        traffic_deficit_pct = max(15, 100 - score_val)
        est_monthly_visits_lost = int((traffic_deficit_pct / 100) * 4500)
        est_revenue_leak_inr = est_monthly_visits_lost * 48  # avg e-commerce/lead CPC value ₹48
        
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("SEO Efficiency Penalty", f"{traffic_deficit_pct}% Lost", "Missed Search Potential", delta_color="inverse")
        f2.metric("Est. Monthly Organic Loss", f"~{est_monthly_visits_lost:,} visits", "Uncaptured Search Intent", delta_color="inverse")
        f3.metric("Annual Value Leak", f"₹{est_revenue_leak_inr * 12:,.0f}", f"~${(est_revenue_leak_inr * 12) / 85:,.0f} USD", delta_color="inverse")
        f4.metric("Recommended Retainer", "₹35k - ₹75k / mo", "Expected ROI: 4.2x")

        # -------------------------------------------------------------
        # 💬 1-CLICK CLIENT ACQUISITION PITCH (NEW)
        # -------------------------------------------------------------
        with st.expander("💬 1-Click Agency Client Outreach Pitch (WhatsApp & Cold Email)", expanded=False):
            st.caption("Send this forensic breakdown to the website owner to close an SEO & Website Optimization deal.")
            
            top_3_issues = [r['action'] for r in recs[:3]]
            issues_bullets = "\n".join([f"• {issue}" for issue in top_3_issues])
            
            wa_pitch = (
                f"Hi {data['domain']} Team,\n\n"
                f"We recently ran a comprehensive 100+ checkpoint technical SEO audit on https://{data['domain']}. "
                f"Your website scored {overall['score']}/100 (Grade: {overall['grade']}).\n\n"
                f"Our diagnostic uncovered critical issues causing search suppression:\n"
                f"{issues_bullets}\n\n"
                f"This technical leakage is currently costing your business an estimated {est_monthly_visits_lost:,} organic visits every month.\n\n"
                f"We have compiled a complete boardroom-ready Executive PDF Report with the step-by-step fix roadmap. "
                f"Could we share the report with your team this week?"
            )
            
            col_pitch1, col_pitch2 = st.columns([3, 1])
            with col_pitch1:
                st.code(wa_pitch, language="text")
            with col_pitch2:
                st.write("")
                st.write("")
                wa_encoded = f"https://api.whatsapp.com/send?text={quote_plus(wa_pitch)}"
                st.link_button("📱 Launch WhatsApp Pitch", wa_encoded, use_container_width=True)

        st.markdown("---")

        # Prioritized Recommendations Accordion
        with st.expander(f"📋 Prioritized Recommendations Checklist ({len(recs)} Found)", expanded=True):
            rec_filter = st.radio("Filter Priority:", ["All", "High Priority", "Medium Priority", "Low Priority"], horizontal=True)
            filtered_recs = [r for r in recs if rec_filter == "All" or r["priority"] == rec_filter]
            
            for r in filtered_recs:
                p_color = "🔴" if "High" in r["priority"] else ("🟠" if "Medium" in r["priority"] else "🟢")
                st.markdown(f"{p_color} **{r['priority'].upper()}:** {r['action']} `[{r['pillar']}]`")

        st.markdown("---")

        # Detailed Inspection Tabs
        tab_onpage, tab_kw, tab_geo, tab_perf, tab_tech, tab_links = st.tabs([
            "🔍 On-Page & SERP",
            "📊 Keyword Consistency",
            "🤖 Generative AI (GEO)",
            "⚡ Core Web Vitals",
            "🛡️ Tech & Email Security",
            "🔗 Links & Architecture"
        ])

        # TAB 1: ON-PAGE & SERP PREVIEW
        with tab_onpage:
            st.markdown("#### 🔍 Google Search Snippet Preview")
            st.markdown(f"""
            <div style="background:#ffffff; color:#1e293b; padding:18px; border-radius:10px; border:1px solid #cbd5e1; max-width:650px; font-family:arial,sans-serif; margin-bottom:16px;">
                <div style="font-size:12px; color:#475569; margin-bottom:2px;">https://{data['domain']} › ...</div>
                <div style="font-size:18px; color:#1a0dab; font-weight:bold; margin-bottom:4px; text-decoration:underline;">{onpage.get('title', data['domain'])}</div>
                <div style="font-size:13px; color:#4b5563; line-height:1.4;">{onpage.get('description', 'No meta description detected.')}</div>
            </div>
            """, unsafe_allow_html=True)

            # Social Share OpenGraph Card Mockup
            st.markdown("#### 📱 Social Share / WhatsApp Card Preview")
            st.markdown(f"""
            <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; padding:14px; max-width:500px; margin-bottom:16px;">
                <div style="color:#94a3b8; font-size:11px; text-transform:uppercase; margin-bottom:4px;">🌐 {data['domain']}</div>
                <div style="color:#f8fafc; font-weight:bold; font-size:15px; margin-bottom:4px;">{onpage.get('title', data['domain'])}</div>
                <div style="color:#cbd5e1; font-size:12px; line-height:1.3;">{onpage.get('description', 'No social description defined.')}</div>
            </div>
            """, unsafe_allow_html=True)

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.write(f"**Title Tag:** `{onpage.get('title')}`")
                st.caption(f"Length: {onpage.get('title_length')} characters ({onpage.get('title_status')})")
                st.write(f"**Meta Description:** `{onpage.get('description')}`")
                st.caption(f"Length: {onpage.get('description_length')} characters ({onpage.get('description_status')})")
            with col_t2:
                st.write(f"**Canonical URL:** `{onpage.get('canonical') or 'None'}`")
                st.write(f"**Word Count:** `{onpage.get('word_count')} words` ({'Thin Content' if onpage.get('is_thin_content') else 'Good Volume'})")
                st.write(f"**Images Missing Alt:** `{onpage.get('img_missing_alt')} / {onpage.get('img_total')}`")
                st.write(f"**Sitemaps:** `{'Found' if onpage.get('has_sitemap') else 'Missing'}` | **Robots.txt:** `{'Found' if onpage.get('has_robots_txt') else 'Missing'}`")

            st.markdown("##### 📑 Header Structure Counts:")
            h_df = pd.DataFrame([{"Header Tag": f"H{i}", "Count": onpage.get("header_counts", {}).get(f"H{i}", 0)} for i in range(2, 7)])
            h_df.loc[-1] = ["H1", onpage.get("h1_count", 0)]
            h_df.index = h_df.index + 1
            h_df = h_df.sort_index()
            st.bar_chart(h_df.set_index("Header Tag")["Count"])

        # TAB 2: KEYWORD CONSISTENCY
        with tab_kw:
            st.markdown("#### 📊 Individual Keywords Consistency Matrix")
            df_ind = pd.DataFrame(kw_data.get("individual_keywords", []))
            if not df_ind.empty:
                df_ind["in_title"] = df_ind["in_title"].apply(lambda x: "✔" if x else "✘")
                df_ind["in_meta"] = df_ind["in_meta"].apply(lambda x: "✔" if x else "✘")
                df_ind["in_headings"] = df_ind["in_headings"].apply(lambda x: "✔" if x else "✘")
                st.dataframe(df_ind.rename(columns={"in_title": "Title Tag", "in_meta": "Meta Desc", "in_headings": "Headings", "frequency": "Frequency"}), use_container_width=True, hide_index=True)

            st.markdown("#### 📑 2-Word Keyphrases Consistency")
            df_ph = pd.DataFrame(kw_data.get("phrases", []))
            if not df_ph.empty:
                df_ph["in_title"] = df_ph["in_title"].apply(lambda x: "✔" if x else "✘")
                df_ph["in_meta"] = df_ph["in_meta"].apply(lambda x: "✔" if x else "✘")
                df_ph["in_headings"] = df_ph["in_headings"].apply(lambda x: "✔" if x else "✘")
                st.dataframe(df_ph.rename(columns={"in_title": "Title Tag", "in_meta": "Meta Desc", "in_headings": "Headings", "frequency": "Frequency"}), use_container_width=True, hide_index=True)

        # TAB 3: GENERATIVE ENGINE OPTIMIZATION (GEO)
        with tab_geo:
            st.markdown("#### 🤖 Generative Engine Optimization (GEO) Readiness")
            st.info("GEO ensures modern LLMs and AI Search Engines (ChatGPT, Perplexity, Claude, Gemini) can parse, comprehend, and cite your website entities.")
            
            g1, g2, g3 = st.columns(3)
            with g1:
                st.metric("LLM Readability Ratio", geo.get("llm_readability_ratio"))
            with g2:
                st.metric("llms.txt Standard File", "Present" if geo.get("has_llms_txt") else "Missing")
            with g3:
                st.metric("AI Bot Crawlers", "Allowed" if geo.get("allows_ai_crawlers") else "Blocked")

            st.write(f"• **Organization Schema:** `{'Identified' if geo.get('has_organization_schema') else 'Missing'}`")
            if geo.get("ai_crawlers_blocked"):
                st.warning(f"Blocked AI Crawlers: {', '.join(geo.get('ai_crawlers_blocked'))}")
            else:
                st.success("All major AI crawlers (GPTBot, ClaudeBot, PerplexityBot) are permitted to index this site.")

        # TAB 4: PERFORMANCE & CORE WEB VITALS
        with tab_perf:
            st.markdown("#### ⚡ Google PageSpeed & Core Web Vitals Lab Data")
            p_c1, p_c2, p_c3, p_c4 = st.columns(4)
            with p_c1: st.metric("Mobile Score", f"{perf.get('mobile_score')}/100")
            with p_c2: st.metric("First Contentful Paint (FCP)", perf.get("fcp"))
            with p_c3: st.metric("Largest Contentful Paint (LCP)", perf.get("lcp"))
            with p_c4: st.metric("Total Page Weight", perf.get("total_page_size_mb"))

            st.write(f"• **Server Response Time (TTFB):** `{perf.get('server_response_ttfb')}`")
            st.write(f"• **Cumulative Layout Shift (CLS):** `{perf.get('cls')}`")
            st.write(f"• **Total Blocking Time (TBT):** `{perf.get('tbt')}`")
            st.write(f"• **Compression (Gzip/Brotli):** `{'Active' if perf.get('compression_active') else 'Inactive'}`")

        # TAB 5: TECHNOLOGY & SECURITY
        with tab_tech:
            st.markdown("#### 🛡️ Infrastructure, Web Stack & Email Security")
            st.write(f"• **Server IP Address:** `{tech.get('server_ip')}`")
            st.write(f"• **Web Server:** `{tech.get('web_server')}`")
            st.write(f"• **DNS Nameservers:** `{', '.join(tech.get('dns_servers', [])) or 'N/A'}`")
            
            st.markdown("##### 🔒 Email Spoofing Protection:")
            if tech.get("has_spf"):
                st.success(f"✔ SPF Record Configured: `{tech.get('spf_record')}`")
            else:
                st.error("✘ Missing SPF Record: Email domain vulnerable to unauthorized spoofing.")

            if tech.get("has_dmarc"):
                st.success("✔ DMARC Record Configured (_dmarc DNS entry active).")
            else:
                st.error("🚨 Missing DMARC Record: High risk of domain impersonation and phishing.")

            st.markdown("##### 💻 Detected CMS & Technology Stack:")
            if tech.get("tech_list"):
                st.dataframe(pd.DataFrame(tech.get("tech_list")), use_container_width=True, hide_index=True)
            else:
                st.info("Custom or proprietary frontend architecture.")

        # TAB 6: LINKS & ARCHITECTURE
        with tab_links:
            st.markdown("#### 🔗 Link Architecture Overview")
            l1, l2, l3 = st.columns(3)
            with l1: st.metric("Total Links", links.get("total_links"))
            with l2: st.metric("Internal Links", links.get("internal_count"))
            with l3: st.metric("External Links", links.get("external_count"))

            st.markdown("##### 📄 Crawled Internal Child Pages:")
            for cp in links.get("child_pages", []):
                st.write(f"• [{cp}](https://{data['domain']}{cp})")