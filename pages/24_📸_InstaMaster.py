import streamlit as st
import pandas as pd
from core.instagram_engine import InstagramMasterEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="InstaMaster | 100+ Point Instagram Audit", page_icon="📸", layout="wide")

# Custom CSS for Agency / Enterprise styling
st.markdown("""
<style>
    .grade-badge {
        font-size: 38px;
        font-weight: 900;
        color: #38bdf8;
        background: #0f172a;
        padding: 10px 20px;
        border-radius: 12px;
        border: 2px solid #0284c7;
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
        background: linear-gradient(135deg, #064e3b, #047857);
        border-radius: 10px;
        padding: 14px;
        color: white;
        text-align: center;
    }
    .collab-card {
        background: #1e293b;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: transform 0.2s ease;
    }
    .collab-card:hover {
        border-color: #60a5fa;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

st.title("📸 InstaMaster: 100+ Point Instagram & Profile OSINT Audit")
st.caption("Commercial Agency-Grade Instagram & Surface-Web Audit • 7 Pillars • 100+ Checkpoints • 5 Collab Suggestions • Zero API Keys")

with st.sidebar:
    st.header("🎯 Target Investigation")
    target_input = st.text_input("Instagram Handle or URL:", value="natgeo", placeholder="e.g. natgeo, mkbhd, cristiano")
    run_btn = st.button("🚀 Run 100+ Point Audit", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("""
    **Audit Capabilities:**
    - 🛰️ Multi-Source OSINT Scraper (Never N/A)
    - 🤝 5 Peer Collab Suggestions & Blueprints
    - 🏛️ 100+ Checkpoint Scorecard (7 Pillars)
    - 💰 Sponsorship Rate Valuation Engine
    - 🔗 Bio Hub Discovery (Linktree, Beacons, etc.)
    - 📄 1-Click Executive PDF Intelligence Report
    """)

if run_btn or "insta_data" not in st.session_state:
    with st.spinner(f"Executing deep OSINT audit on '@{target_input}' across open search indexes & surface web..."):
        engine = InstagramMasterEngine()
        data = engine.audit_profile(target_input)
        st.session_state["insta_data"] = data
        st.session_state["insta_target"] = target_input

if "insta_data" in st.session_state:
    data = st.session_state["insta_data"]

    if data.get("error"):
        st.error(f"⚠️ {data['error']}")
    else:
        # 1. TOP HEADER & EXECUTIVE SCORECARD
        h_col1, h_col2, h_col3, h_col4 = st.columns([1.2, 3, 2, 2])
        
        with h_col1:
            if data.get("avatar_url"):
                st.image(data["avatar_url"], width=120)
            else:
                st.markdown("### 👤")

        with h_col2:
            verif_badge = " ✅ Verified" if data.get("is_verified") else ""
            st.subheader(f"{data['full_name']} (@{data['username']}){verif_badge}")
            st.markdown(f"🏷️ **Niche:** `{data.get('niche', 'General')}` | **Tier:** `{data.get('tier', 'Standard')}`")
            st.caption(f"📡 Intelligence Source: `{data.get('source_layer', 'Surface Index')}`")
            st.markdown(f"🔗 [View Profile on Instagram]({data['profile_url']})")

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
                pdf_bytes = pdf_gen.generate_instagram_pdf(data)
                if pdf_bytes:
                    st.download_button(
                        "📄 Download 100+ Audit PDF",
                        pdf_bytes,
                        file_name=f"{data['username']}_Instagram_100_Audit.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )

        st.markdown("---")

        # 2. CORE AUDIENCE & AUTHORITY METRICS
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Followers", data["followers_str"], f"{data['followers_raw']:,} exact" if data['followers_raw'] else "Surface Web")
        m2.metric("Following", data["following_str"], f"{data['following_raw']:,} exact" if data['following_raw'] else "Surface Web")
        m3.metric("Total Posts", data["posts_str"], f"{data['posts_raw']:,} exact" if data['posts_raw'] else "Surface Web")
        m4.metric("Authority Ratio", f"{data['authority_ratio']}:1", "Followers / Following")

        st.markdown("---")

        # 3. COLLABORATION SUGGESTIONS (5 SAME-TYPE CREATORS)
        st.subheader("🤝 5 Same-Type Creator Collaboration Suggestions")
        st.caption("Hand-matched high-synergy peers in the same niche for co-creation, audience expansion, and cross-promotion.")

        collab_list = data.get("collab_suggestions", [])
        if collab_list:
            c_cols = st.columns(len(collab_list))
            for idx, c in enumerate(collab_list):
                with c_cols[idx]:
                    st.markdown(f"""
                    <div class="collab-card">
                        <div style="font-size: 24px; margin-bottom: 4px;">👑</div>
                        <div style="font-weight: 700; font-size: 15px; color: #f8fafc;">{c['name']}</div>
                        <div style="font-size: 12px; color: #38bdf8;">@{c['handle']}</div>
                        <div style="font-size: 11px; color: #94a3b8; margin: 4px 0;">{c['tier']}</div>
                        <div style="background: #0f172a; padding: 4px 8px; border-radius: 6px; font-size: 11px; color: #22c55e; font-weight: bold; margin: 6px 0;">
                            🔥 {c['match_score']}% Synergy Match
                        </div>
                        <div style="font-size: 11px; color: #cbd5e1; margin-top: 6px;">
                            <b>Strategy:</b> {c['strategy']}<br>
                            <b>Format:</b> {c['format']}<br>
                            <b>Reach Boost:</b> {c['reach_multiplier']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.link_button(f"View @{c['handle']}", c['profile_url'], use_container_width=True)
        else:
            st.info("No collab peers matched for this specific niche.")

        st.markdown("---")

        # 4. COMMERCIAL RATE CARD & MONETIZATION VALUATION
        st.subheader("💰 Commercial Rate Card & Sponsorship Valuation")
        st.caption("Standard agency sponsorship projections based on follower liquidity and creator tier benchmarks.")
        rates = data.get("commercial_rates", {})
        
        r1, r2, r3, r4 = st.columns(4)
        r1.markdown(f"""<div class="rate-card"><h4>Feed Post</h4><h2>${rates.get('sponsored_post_low', 0):,} - ${rates.get('sponsored_post_high', 0):,}</h2><span>per sponsored post</span></div>""", unsafe_allow_html=True)
        r2.markdown(f"""<div class="rate-card"><h4>Dedicated Reel</h4><h2>${rates.get('sponsored_reel', 0):,}</h2><span>per 60s Reel</span></div>""", unsafe_allow_html=True)
        r3.markdown(f"""<div class="rate-card"><h4>Story Sequence</h4><h2>${rates.get('sponsored_story', 0):,}</h2><span>per 3-frame set</span></div>""", unsafe_allow_html=True)
        r4.markdown(f"""<div class="rate-card" style="background: linear-gradient(135deg, #1e3a8a, #2563eb);"><h4>Annual Capacity</h4><h2>${rates.get('annual_potential', 0):,}</h2><span>est. sponsor potential</span></div>""", unsafe_allow_html=True)

        st.markdown("---")

        # 5. 7-PILLAR SCORECARD BREAKDOWN
        st.subheader("🏛️ 7-Pillar Technical & Commercial Scorecard")
        categories = data.get("categories", {})
        
        p_cols = st.columns(len(categories) if categories else 1)
        for idx, (cat_name, cat_val) in enumerate(categories.items()):
            with p_cols[idx]:
                st.markdown(f"**{cat_name.split('&')[0].strip()}**")
                st.progress(cat_val["pct"] / 100.0)
                st.write(f"**Grade:** `{cat_val['grade']}` ({cat_val['passed']}/{cat_val['total']})")

        st.markdown("---")

        # 6. BIO HUBS & CROSS-PLATFORM FOOTPRINT
        b_col, cp_col = st.columns(2)

        with b_col:
            st.markdown("### 🔗 Creator Bio Hubs & Landing Pages")
            bio_links = data.get("bio_links", [])
            if bio_links:
                for bl in bio_links:
                    st.success(f"🟢 **{bl['name']}:** [{bl['url']}]({bl['url']}) (Active landing page)")
            else:
                st.info("⚪ No external bio landing hubs (Linktree, Beacons, Stan Store, etc.) detected under this username.")

            if data.get("bio"):
                st.markdown("#### 📝 Surface Bio Snippet")
                st.info(data["bio"])

        with cp_col:
            st.markdown("### 🌐 Cross-Platform OSINT Identity Mapping")
            st.caption("Validates if the exact same handle exists across social and creator networks.")
            cp_list = data.get("cross_platform", [])
            if cp_list:
                df_cp = pd.DataFrame(cp_list)
                df_cp["Status"] = df_cp["exists"].apply(lambda x: "🟢 Active / Found" if x else "⚪ Not Found")
                df_cp = df_cp[["name", "Status", "url"]].rename(columns={"name": "Platform", "url": "URL"})
                st.dataframe(df_cp, use_container_width=True, hide_index=True)

        st.markdown("---")

        # 7. ACTIONABLE ROADMAP RECOMMENDATIONS
        st.subheader("⚡ High-Priority Optimization Roadmap")
        recs = data.get("recommendations", [])
        if recs:
            for r in recs:
                st.warning(f"**[{r['priority']}] {r['title']} ({r['category']}):** {r['recommendation']}")
        else:
            st.success("🎉 Outstanding profile! All core checkpoints passed with zero critical warnings.")

        st.markdown("---")

        # 8. INTERACTIVE 100+ CHECKPOINT AUDIT LOG
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