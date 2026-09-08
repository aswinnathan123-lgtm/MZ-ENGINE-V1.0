import streamlit as st
import pandas as pd
from core.youtube_seo_engine import YouTubeMasterEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(
    page_title="YouTubeMaster | 100+ Point Channel & Video SEO Audit",
    page_icon="📺",
    layout="wide"
)

# Custom Enterprise CSS
st.markdown("""
<style>
    .grade-badge {
        font-size: 38px;
        font-weight: 900;
        color: #ef4444;
        background: #0f172a;
        padding: 10px 22px;
        border-radius: 12px;
        border: 2px solid #dc2626;
        display: inline-block;
        text-align: center;
    }
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }
    .rate-card {
        background: linear-gradient(135deg, #7f1d1d, #b91c1c);
        border-radius: 10px;
        padding: 14px;
        color: white;
        text-align: center;
    }
    .collab-box {
        background: #1e293b;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📺 YouTubeMaster: 100+ Point Channel & Video SEO Audit")
st.caption("Commercial Agency-Grade YouTube Channel & Algorithm Engine • 7 Pillars • 100+ Checkpoints • 5 Collab Suggestions • Real-Time Autocomplete SEO • Zero API Keys")

with st.sidebar:
    st.header("🎯 Target Investigation")
    target_input = st.text_input(
        "YouTube Channel Handle or URL:",
        value="@mkbhd",
        placeholder="e.g. @mkbhd, @veritasium, MrBeast, or channel URL"
    )
    run_btn = st.button("🚀 Run 100+ Point Audit", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("""
    **Audit Scope (100+ Checks across 7 Pillars):**
    - 🏛️ Channel Branding & Architecture (15 checks)
    - 🎯 Title, Hook & CTR Engineering (15 checks)
    - 📝 Description & Timestamp Funnel (15 checks)
    - 🔍 Search Indexing & Autocomplete SEO (15 checks)
    - 🖼️ Thumbnail Visual Forensics (10 checks)
    - 📈 Retention, Playlists & Momentum (15 checks)
    - 💰 Commercial CPM & Rate Card (15 checks)
    
    **Features:**
    - 🤝 5 Same-Type Creator Collab Suggestions
    - ⚡ Real-Time Suggest Query Keywords
    - 📄 Executive PDF Audit Download
    """)

if run_btn or "yt_data" not in st.session_state:
    with st.spinner(f"Auditing YouTube channel '{target_input}' across open web & algorithm surfaces..."):
        engine = YouTubeMasterEngine()
        data = engine.audit_channel(target_input)
        st.session_state["yt_data"] = data
        st.session_state["yt_target"] = target_input

if "yt_data" in st.session_state:
    data = st.session_state["yt_data"]

    if data.get("error"):
        st.error(f"⚠️ {data['error']}")
    else:
        # -------------------------------------------------------------
        # 0. CHANNEL BANNER (If available)
        # -------------------------------------------------------------
        if data.get("banner_url"):
            st.image(data["banner_url"], use_container_width=True)

        # -------------------------------------------------------------
        # 1. TOP HEADER & EXECUTIVE SCORECARD
        # -------------------------------------------------------------
        h_col1, h_col2, h_col3, h_col4 = st.columns([1.2, 3, 2, 2])
        
        with h_col1:
            if data.get("avatar_url"):
                st.image(data["avatar_url"], width=130)
            else:
                st.markdown("### 📺")

        with h_col2:
            st.subheader(f"{data.get('channel_title', 'Channel')} (@{data.get('handle', '')})")
            niche = data.get('niche', 'General')
            country = data.get('country', 'Global')
            joined = data.get('joined_date', 'N/A')
            st.markdown(f"🏷️ **Niche:** `{niche}` | 🌍 **Country:** `{country}`")
            if joined and joined != 'N/A':
                st.markdown(f"📅 **Joined:** `{joined}`")
            st.markdown(f"🔗 [Open YouTube Channel]({data.get('channel_url', '#')})")

        with h_col3:
            st.markdown(f"""
            <div class="grade-badge">
                {data.get('overall_grade', 'N/A')}<br>
                <span style="font-size: 13px; color: #94a3b8;">{data.get('overall_score', 0)}% Score</span>
            </div>
            """, unsafe_allow_html=True)

        with h_col4:
            st.metric("Audit Checks Passed", f"{data.get('passed_checks', 0)} / {data.get('total_checks', 100)}")
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_youtube_pdf(data)
                if pdf_bytes:
                    st.download_button(
                        "📄 Download 100+ Audit PDF",
                        pdf_bytes,
                        file_name=f"{data.get('handle', 'youtube')}_YouTube_100_Audit.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )

        st.markdown("---")

        # -------------------------------------------------------------
        # 2. CORE CHANNEL & VIDEO METRICS
        # -------------------------------------------------------------
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Subscribers", data.get("subscribers_str", "N/A"), f"{data.get('subscribers_count', 0):,} exact" if data.get('subscribers_count') else "Surface Web")
        m2.metric("Total Views", data.get("views_str", "N/A"), f"{data.get('total_views', 0):,} total" if data.get('total_views') else "Surface Web")
        m3.metric("Video Count", data.get("videos_str", "N/A"), f"{data.get('video_count', 0):,} published" if data.get('video_count') else "Surface Web")
        
        # Avg Views / Video
        avg_v = 0
        if data.get('video_count') and data.get('total_views'):
            avg_v = int(data['total_views'] / max(1, data['video_count']))
            m4.metric("Avg Views / Video", f"{avg_v:,}", "Lifetime Benchmark")
        else:
            m4.metric("Avg Views / Video", "N/A", "Calculation Pending")


        # -------------------------------------------------------------
        # 2.5 REAL-TIME VIEW TRAFFIC & 7D / 30D VELOCITY FORENSICS
        # -------------------------------------------------------------
        st.subheader("📈 Real-Time View Traffic & Velocity Forensics")
        st.caption("Algorithmic view velocity run-rates (7-day, 30-day), real-time VPH, and traffic acquisition breakdown.")
        traffic = data.get("view_traffic", {})

        v1, v2, v3, v4 = st.columns(4)
        v1.metric("7 Days Views", traffic.get("views_7d_str", "N/A"), f"{traffic.get('views_7d', 0):,} weekly run-rate")
        v2.metric("30 Days Views", traffic.get("views_30d_str", "N/A"), f"{traffic.get('views_30d', 0):,} monthly volume")
        v3.metric("Daily Run-Rate", traffic.get("daily_views_str", "N/A"), "Avg daily velocity")
        v4.metric("Live Hourly Velocity", traffic.get("vph_str", "N/A"), "Views-Per-Hour (VPH)")

        vt_col1, vt_col2 = st.columns([1.5, 1])

        with vt_col1:
            st.markdown("#### 🧭 Traffic Source Acquisition Distribution")
            sources = traffic.get("traffic_sources", {})
            if sources:
                for src_name, pct in sources.items():
                    st.write(f"**{src_name}**: `{pct}%`")
                    st.progress(pct / 100.0)

        with vt_col2:
            st.markdown("#### ⚡ Algorithmic Momentum & Liquidity")
            st.info(f"**Status:** {traffic.get('momentum_status', 'Active')}")
            st.markdown(f"📊 **Views-to-Subscriber Liquidity Ratio:** `{traffic.get('liquidity_ratio', 0)}x`")
            st.markdown(f"🗓️ **Projected 90-Day Views:** `{traffic.get('projected_90d', 'N/A')}`")
            st.markdown(f"🚀 **Projected 1-Year Annual Views:** `{traffic.get('projected_annual', 'N/A')}`")

        st.markdown("---")

        # -------------------------------------------------------------
        # 3. COMMERCIAL RATE CARD & SPONSORSHIP VALUATION
        # -------------------------------------------------------------
        st.subheader("💰 Commercial Rate Card & Sponsorship Valuation")
        st.caption("Standard commercial advertising rates calculated from subscriber volume, CPM market tier, and viewer liquidity.")
        rates = data.get("commercial_rates", {})
        
        r1, r2, r3, r4 = st.columns(4)
        r1.markdown(f"""<div class="rate-card"><h4>Dedicated Video</h4><h2>${rates.get('dedicated_video_low', 0):,} - ${rates.get('dedicated_video_high', 0):,}</h2><span>per sponsored feature</span></div>""", unsafe_allow_html=True)
        r2.markdown(f"""<div class="rate-card"><h4>60s Mid-Roll</h4><h2>${rates.get('midroll_integration', 0):,}</h2><span>per 60s integration</span></div>""", unsafe_allow_html=True)
        r3.markdown(f"""<div class="rate-card"><h4>YouTube Short</h4><h2>${rates.get('short_integration', 0):,}</h2><span>per vertical short</span></div>""", unsafe_allow_html=True)
        r4.markdown(f"""<div class="rate-card" style="background: linear-gradient(135deg, #1e3a8a, #2563eb);"><h4>Annual Capacity</h4><h2>${rates.get('annual_deal_potential', 0):,}</h2><span>est. brand deal potential</span></div>""", unsafe_allow_html=True)

        st.markdown("---")

        # -------------------------------------------------------------
        # 4. 5 SAME-TYPE CREATOR COLLABORATION SUGGESTIONS
        # -------------------------------------------------------------
        st.subheader("🤝 5 High-Synergy Same-Type Creator Collaboration Matches")
        st.caption("Algorithmically matched creators in the same niche for audience crossover, co-production, and view velocity boosts.")
        collabs = data.get("collab_suggestions", [])
        if collabs:
            for idx, c in enumerate(collabs[:5]):
                with st.container():
                    st.markdown(f"""
                    <div class="collab-box">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: #38bdf8;">#{idx+1} {c.get('name')} (@{c.get('handle')})</h4>
                            <span style="background: #15803d; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px;">
                                {c.get('match_score')}% Niche Match
                            </span>
                        </div>
                        <p style="margin: 6px 0; color: #cbd5e1;"><b>Audience Base:</b> {c.get('subscribers')} Subscribers</p>
                        <p style="margin: 4px 0; color: #94a3b8;"><b>💡 Recommended Strategy:</b> {c.get('strategy')}</p>
                        <p style="margin: 4px 0; color: #e2e8f0;"><b>🎬 Recommended Format:</b> <code>{c.get('format')}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No collaboration matches generated for this channel.")

        st.markdown("---")

        # -------------------------------------------------------------
        # 5. REAL-TIME SEARCH QUERY KEYWORD TREE (YouTube Suggest)
        # -------------------------------------------------------------
        st.subheader("⚡ Real-Time YouTube Search Autocomplete Keywords")
        st.caption("Live keyword search phrases directly extracted from YouTube's autocomplete search suggestions for maximum discoverability.")
        kw_opps = data.get("keyword_opportunities", [])
        if kw_opps:
            df_kw = pd.DataFrame(kw_opps)
            df_kw = df_kw.rename(columns={
                "keyword": "Search Term",
                "type": "Intent Archetype",
                "source": "Suggestion Source"
            })
            st.dataframe(df_kw, use_container_width=True, hide_index=True)
        else:
            st.info("No keyword suggestions retrieved.")

        st.markdown("---")

        # -------------------------------------------------------------
        # 6. 7-PILLAR SCORECARD BREAKDOWN
        # -------------------------------------------------------------
        st.subheader("🏛️ 7-Pillar Algorithmic & Technical Scorecard")
        categories = data.get("categories", {})
        
        p_cols = st.columns(len(categories) if categories else 1)
        for idx, (cat_name, cat_val) in enumerate(categories.items()):
            with p_cols[idx]:
                st.markdown(f"**{cat_name.split('&')[0].strip()}**")
                st.progress(cat_val["pct"] / 100.0)
                st.write(f"**Grade:** `{cat_val['grade']}` ({cat_val['passed']}/{cat_val['total']})")

        st.markdown("---")

        # -------------------------------------------------------------
        # 7. HIGH-PRIORITY ROADMAP RECOMMENDATIONS
        # -------------------------------------------------------------
        st.subheader("⚡ High-Priority Optimization Roadmap")
        recs = data.get("recommendations", [])
        if recs:
            for r in recs:
                st.warning(f"**[{r['priority']}] {r['title']} ({r['category']}):** {r['recommendation']}")
        else:
            st.success("🎉 Outstanding channel architecture! All core checkpoints passed with zero critical warnings.")

        st.markdown("---")

        # -------------------------------------------------------------
        # 8. INTERACTIVE 100+ CHECKPOINT AUDIT LOG
        # -------------------------------------------------------------
        st.subheader("📋 Complete 100+ Checkpoint Audit Log")
        
        filter_col1, filter_col2 = st.columns([2, 2])
        with filter_col1:
            cat_filter = st.selectbox("Filter by Pillar:", ["All Pillars"] + list(categories.keys()))
        with filter_col2:
            status_filter = st.selectbox("Filter by Status:", ["All Statuses", "PASS", "WARNING", "FAIL"])

        checkpoints = data.get("checkpoints", [])
        filtered_checks = checkpoints
        if cat_filter != "All Pillars":
            filtered_checks = [c for c in filtered_checks if c["category"] == cat_filter]
        if status_filter != "All Statuses":
            filtered_checks = [c for c in filtered_checks if c["status"] == status_filter]

        st.markdown(f"*Displaying **{len(filtered_checks)}** of **{len(checkpoints)}** checkpoints:*")

        df_checks = pd.DataFrame(filtered_checks)
        if not df_checks.empty:
            df_display = df_checks[["id", "category", "name", "status", "score", "max_score", "detail"]].rename(
                columns={"id": "#", "category": "Pillar", "name": "Checkpoint", "status": "Status", "score": "Pts", "max_score": "Max", "detail": "Diagnostic Findings"}
            )
            st.dataframe(df_display, use_container_width=True, hide_index=True)
