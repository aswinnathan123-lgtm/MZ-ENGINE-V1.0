import streamlit as st
import pandas as pd
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

POPULAR_SITES = ["shrinithiinfra.in", "casagrand.co.in", "stripe.com", "apple.com", "netflix.com"]

with st.sidebar:
    st.header("🎯 Audit Target")
    site_choice = st.selectbox("Quick Select Site:", POPULAR_SITES, index=0)
    custom_target = st.text_input("Or Enter Any Website URL:", value="", placeholder="e.g. yourclient.com")
    active_target = custom_target.strip() if custom_target else site_choice
    
    st.markdown("---")
    st.header("🏢 Agency Branding")
    agency_brand = st.text_input("Report Agency Name:", value="NASA OSINT Intelligence")
    
    run_btn = st.button("🚀 Run Comprehensive 100+ Audit", type="primary", use_container_width=True)

if run_btn or "agency_seo_data" not in st.session_state:
    with st.spinner(f"Running deep 100+ checkpoint audit for {active_target}..."):
        engine = AgencySEOEngine()
        data = engine.run_comprehensive_audit(active_target)
        st.session_state["agency_seo_data"] = data
        st.session_state["agency_seo_active"] = active_target

if "agency_seo_data" in st.session_state:
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

        # Header Scorecard & PDF Export Button
        c_head1, c_head2, c_head3 = st.columns([2, 2, 1.5])
        with c_head1:
            st.subheader(f"🌐 Audit: {data['domain']}")
            st.caption(f"Target URL: `{data['full_url']}` • Checked on {data['timestamp']}")
        with c_head2:
            st.metric("Overall Health Grade", f"{overall['grade']} ({overall['score']}/100)", f"{len(recs)} Recommendations")
        with c_head3:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_agency_seo_audit_pdf(data["domain"], data, agency_name=agency_brand)
                if pdf_bytes:
                    st.download_button(
                        "📄 Download White-Label PDF",
                        pdf_bytes,
                        f"{data['domain']}_Executive_SEO_Report.pdf",
                        "application/pdf",
                        type="primary",
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
