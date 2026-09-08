import urllib.parse
import pandas as pd
import streamlit as st
from core.instagram_engine import InstagramMasterEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(
    page_title="InstaMaster | Advanced Instagram & RTN OSINT Suite",
    page_icon="📸",
    layout="wide"
)

# Custom Agency / Enterprise styling
st.markdown("""
<style>
    .grade-badge {
        font-size: 40px;
        font-weight: 900;
        color: #38bdf8;
        background: #0f172a;
        padding: 10px 22px;
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
    .rtn-box {
        background-color: #0f172a;
        border: 1px solid #38bdf8;
        border-radius: 10px;
        padding: 18px;
        color: #f8fafc;
        margin-bottom: 16px;
    }
    .tag-chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📸 InstaMaster: Advanced Instagram OSINT, Retention & RTN Script Suite")
st.caption("100+ Checkpoints • Follower Churn Forensics • Reel Watch Retention • Profile Name OSINT Strength • Trending Assets • RTN Script Maker")

# =====================================================================
# SIDEBAR CONTROLS & POPULAR CREATOR CHIPS
# =====================================================================
POPULAR_CREATORS = ["natgeo", "mkbhd", "cristiano", "mrwhosetheboss", "hubermanlab", "codiesanchez", "gordongram"]

with st.sidebar:
    st.header("🎯 Target Investigation")
    quick_choice = st.selectbox("Quick-Select Popular Creator:", POPULAR_CREATORS, index=0)
    target_input = st.text_input("Or Enter Any Instagram Handle / URL:", value="", placeholder="e.g. natgeo, mkbhd, yourbrand")
    active_target = target_input.strip() if target_input.strip() else quick_choice

    run_btn = st.button("🚀 Run Advanced OSINT Audit", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("""
    **Advanced OSINT Scope:**
    - 📈 **Follower Drop/Gain & Churn**: 30-day velocity, bot risk
    - ⏱️ **Watch Time & Retention**: Hook hold rate, completion %
    - 🔍 **Profile Name Strength**: Search SEO & namespace purity
    - 📌 **Top Trending Captions**: Viral save multipliers
    - 🎵 **Top Trending Audios**: Surging sound velocity
    - 🎬 **Top Trending Reels**: Niche viral frameworks
    - 🎬 **RTN Script Maker**: Retention-engineered video scripts
    """)

# =====================================================================
# DATA RETRIEVAL & SESSION STATE CACHING
# =====================================================================
if run_btn or "insta_data" not in st.session_state or st.session_state.get("insta_active_handle") != active_target:
    with st.spinner(f"Executing deep multi-source OSINT audit on '@{active_target}'..."):
        engine = InstagramMasterEngine()
        data = engine.audit_profile(active_target)
        st.session_state["insta_data"] = data
        st.session_state["insta_active_handle"] = active_target

# =====================================================================
# MAIN DASHBOARD INTERFACE
# =====================================================================
if "insta_data" in st.session_state:
    data = st.session_state["insta_data"]

    if data.get("error"):
        st.error(f"⚠️ {data['error']}")
    else:
        growth = data.get("growth_forensics", {})
        retention = data.get("view_time_retention", {})
        name_osint = data.get("name_strength", {})
        captions = data.get("trending_captions", [])
        audios = data.get("trending_audios", [])
        reels = data.get("trending_reels", [])
        rtn_scripts = data.get("rtn_scripts", [])

        # -------------------------------------------------------------
        # 1. TOP HEADER & EXECUTIVE SCORECARD
        # -------------------------------------------------------------
        h_col1, h_col2, h_col3, h_col4 = st.columns([1.2, 3, 2, 2])
        
        with h_col1:
            if data.get("avatar_url"):
                st.image(data["avatar_url"], width=130)
            else:
                st.markdown("### 👤")

        with h_col2:
            verif_badge = " ✅ Verified" if data.get("is_verified") else ""
            st.subheader(f"{data['full_name']} (@{data['username']}){verif_badge}")
            st.markdown(f"🏷️ **Niche:** `{data.get('niche', 'General')}` | **Tier:** `{data.get('tier', 'Standard')}`")
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
                        "📄 Download Audit PDF",
                        pdf_bytes,
                        file_name=f"{data['username']}_Instagram_100_Audit.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
            else:
                st.caption("PDF Ready")

        st.markdown("---")

        # -------------------------------------------------------------
        # 2. ADVANCED FORENSICS TRIFECTA: GROWTH, RETENTION & NAME OSINT
        # -------------------------------------------------------------
        st.subheader("🛰️ Advanced Profile Forensics & Intelligence Diagnostics")

        f_col1, f_col2, f_col3 = st.columns(3)

        # BOX 1: FOLLOWER DROP / GAIN & CHURN FORENSICS
        with f_col1:
            st.markdown("#### 📈 Follower Churn & Velocity")
            st.metric("Net Daily Growth", growth.get("daily_gain_est", "N/A"), growth.get("monthly_gain_est", "30d projection"))
            st.write(f"• **Estimated Churn Rate:** `{growth.get('monthly_churn_pct', '1.8%')}`")
            st.write(f"• **Daily Lost Followers:** `{growth.get('daily_lost_est', 'N/A')}`")
            st.write(f"• **Bot Purge Vulnerability:** `{growth.get('bot_purge_risk', 'Low')}`")
            st.info(f"🎯 **Next Target Milestone:** `{growth.get('target_milestone')}` in **{growth.get('days_to_milestone')}**")

        # BOX 2: POST VIEW TIME & WATCH RETENTION FORENSICS
        with f_col2:
            st.markdown("#### ⏱️ Post View Time & Retention")
            st.metric("Avg Reel Watch Time", f"{retention.get('avg_watch_time', '10.2s')} / {retention.get('median_duration', '15s')}", f"{retention.get('completion_pct', '68%')} Completion")
            st.write(f"• **Hook Hold Rate (0-3s):** `{retention.get('hook_hold_rate_3s', '78%')}`")
            st.write(f"• **Rewatch & Loop Multiplier:** `{retention.get('loop_multiplier', '1.25x')}`")
            st.write(f"• **Drop-off Danger Zone:** `{retention.get('dropoff_zone', 'Sec 3.5')}`")
            st.success(f"{retention.get('retention_tier', 'Tier 2 Algorithm Reach')}")

        # BOX 3: PROFILE NAME STRENGTH (USE OSINT)
        with f_col3:
            st.markdown("#### 🔍 Profile Name OSINT Strength")
            st.metric("Name Authority Score", f"{name_osint.get('score', 75)} / 100", name_osint.get("badge", "Strong"))
            for find in name_osint.get("findings", [])[:3]:
                st.write(f"• {find}")
            st.warning(f"💡 **Optimization:** {name_osint.get('recommendation', 'Add primary keyword to display name.')}")

        st.markdown("---")

        # -------------------------------------------------------------
        # 3. CORE STATS & COMMERCIAL VALUATION
        # -------------------------------------------------------------
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Followers", data["followers_str"], f"{data['followers_raw']:,} exact" if data['followers_raw'] else "Surface Web")
        m2.metric("Following", data["following_str"], f"{data['following_raw']:,} exact" if data['following_raw'] else "Surface Web")
        m3.metric("Total Posts", data["posts_str"], f"{data['posts_raw']:,} exact" if data['posts_raw'] else "Surface Web")
        m4.metric("Authority Ratio", f"{data['authority_ratio']}:1", "Followers / Following")

        rates = data.get("commercial_rates", {})
        r1, r2, r3, r4 = st.columns(4)
        r1.markdown(f"""<div class="rate-card"><h4>Feed Post</h4><h2>${rates.get('sponsored_post_low', 0):,} - ${rates.get('sponsored_post_high', 0):,}</h2><span>per sponsored post</span></div>""", unsafe_allow_html=True)
        r2.markdown(f"""<div class="rate-card"><h4>Dedicated Reel</h4><h2>${rates.get('sponsored_reel', 0):,}</h2><span>per 60s Reel</span></div>""", unsafe_allow_html=True)
        r3.markdown(f"""<div class="rate-card"><h4>Story Sequence</h4><h2>${rates.get('sponsored_story', 0):,}</h2><span>per 3-frame set</span></div>""", unsafe_allow_html=True)
        r4.markdown(f"""<div class="rate-card" style="background: linear-gradient(135deg, #1e3a8a, #2563eb);"><h4>Annual Capacity</h4><h2>${rates.get('annual_potential', 0):,}</h2><span>est. sponsor potential</span></div>""", unsafe_allow_html=True)

        st.markdown("---")

        # =============================================================
        # 4. FIVE DEDICATED WORKSPACE TABS
        # =============================================================
        tab_trending, tab_rtn, tab_retention, tab_collabs, tab_audit = st.tabs([
            "🔥 Trending Captions, Audios & Reels",
            "🎬 RTN Viral Script Maker",
            "⏱️ Watch Retention & Churn Forensics",
            "🤝 Collab Matches & Bio Hubs",
            "📋 100+ Checkpoint Audit Log"
        ])

        # -------------------------------------------------------------
        # TAB 1: TRENDING CAPTIONS, AUDIOS & REELS (USER REQUEST)
        # -------------------------------------------------------------
        with tab_trending:
            st.markdown(f"### 🔥 Niche Outlier Creative Radar: `{data.get('niche')}`")
            st.caption("Side-by-side intelligence tables: Top trending captions with saves multipliers, surging audios, and viral reel concepts.")

            c_col1, c_col2 = st.columns(2)

            with c_col1:
                st.markdown("#### 📌 Table: Top Trending Captions")
                for c_item in captions:
                    with st.expander(f"{c_item.get('hook_type')} • {c_item.get('save_multiplier')}", expanded=True):
                        st.code(c_item.get("caption_text"), language="markdown")
                        st.caption(f"**CTA Strategy:** `{c_item.get('cta_strategy')}` • **Length:** `{c_item.get('char_length')}`")

            with c_col2:
                st.markdown("#### 🎵 Table: Top Trending Audios")
                for a_item in audios:
                    with st.container():
                        st.markdown(f"##### 🎶 {a_item.get('sound_name')}")
                        st.write(f"**Artist:** `{a_item.get('artist')}` • **Velocity:** `{a_item.get('velocity_badge')}`")
                        st.write(f"• **Volume:** `{a_item.get('est_reels_count')}` • **Best Format:** `{a_item.get('recommended_format')}`")
                        st.markdown(f"[🔍 Open Sound Search on Instagram](https://www.instagram.com/reels/)")
                        st.markdown("---")

            st.markdown("#### 🎬 List: Top Trending Reels in this Niche")
            for r_item in reels:
                with st.expander(f"🎥 {r_item.get('title')} ({r_item.get('duration')})", expanded=True):
                    r_c1, r_c2 = st.columns([3, 1])
                    with r_c1:
                        st.write(f"**Framework:** `{r_item.get('framework')}`")
                        st.write(f"**Hook Concept:** {r_item.get('hook_concept')}")
                    with r_c2:
                        st.metric("Benchmark Views", r_item.get("est_benchmark_views"))
                        st.markdown(f"[🔗 View Explorer Tag]({r_item.get('search_query')})")

        # -------------------------------------------------------------
        # TAB 2: LINK TO RTN SCRIPT MAKER (USER REQUEST)
        # -------------------------------------------------------------
        with tab_rtn:
            st.markdown("### 🎬 RTN (Retention-Targeted Narrative) Viral Script Maker")
            st.caption(f"Advanced OSINT-generated short-form video scripts engineered specifically for **@{data['username']}** in the **{data.get('niche')}** vertical.")

            st.info("💡 **RTN Architecture:** Hooks the viewer in 0-3 seconds, opens a curiosity loop in 3-8 seconds, delivers high-speed value with jump cuts every 2.5s, and seamlessly loops the audio back to the beginning.")

            for s_idx, script in enumerate(rtn_scripts, 1):
                with st.expander(f"{script.get('title')} ({script.get('target_duration')})", expanded=(s_idx == 1)):
                    st.markdown(f"**Objective:** `{script.get('objective')}`")
                    st.markdown("##### 📝 Teleprompter-Ready Script Text:")
                    st.text_area(
                        "Copy Teleprompter Script:",
                        script.get("teleprompter_text"),
                        height=220,
                        key=f"rtn_script_box_{s_idx}"
                    )
                    st.markdown("##### 🎥 Director Pacing & B-Roll Notes:")
                    for note in script.get("production_notes", []):
                        st.write(f"• {note}")

            st.markdown("---")
            st.markdown("#### 🚀 Direct Links to Companion Growth Tools")
            link_c1, link_c2, link_c3 = st.columns(3)
            with link_c1:
                st.markdown("[🪝 Open HookStudio (300+ Viral Hooks)](1_🪝_HookStudio)")
                st.caption("Generate infinite first-3-second visual and audio hooks.")
            with link_c2:
                st.markdown("[🎯 Open ClientHunter (Local Video Pack)](27_🎯_ClientHunter)")
                st.caption("Package RTN scripts into high-ticket $2,000/mo retainer deals.")
            with link_c3:
                st.markdown("[🤖 Open AISynthesizer (Full Content Pack)](20_🤖_AISynthesizer)")
                st.caption("Expand scripts into multi-platform carousels and threads.")

        # -------------------------------------------------------------
        # TAB 3: WATCH RETENTION & FOLLOWER CHURN FORENSICS
        # -------------------------------------------------------------
        with tab_retention:
            st.markdown("### ⏱️ Video Watch Time Retention & Churn Dynamics")

            r_col1, r_col2 = st.columns(2)

            with r_col1:
                st.markdown("#### 📉 Reel Second-by-Second Viewer Retention Funnel")
                df_funnel = pd.DataFrame(retention.get("funnel_table", []))
                if not df_funnel.empty:
                    st.dataframe(df_funnel, use_container_width=True, hide_index=True)

                st.markdown("#### 🎯 4 Rules to Fix the Second 3.5 Hook Cliff")
                for tip in retention.get("pacing_tips", []):
                    st.write(f"• {tip}")

            with r_col2:
                st.markdown("#### 📅 7-Day Follower Trajectory & Inflow Log")
                df_traj = pd.DataFrame(growth.get("trajectory_table", []))
                if not df_traj.empty:
                    st.dataframe(df_traj, use_container_width=True, hide_index=True)

                st.markdown("#### 🛡️ Organic Audience Health Assessment")
                st.write(f"• **Follower-to-Following Ratio:** `{data.get('authority_ratio')}:1`")
                st.write(f"• **Bot Purge Susceptibility:** `{growth.get('bot_purge_risk')}`")
                st.write(f"• **Estimated Daily Churn:** `{growth.get('daily_lost_est')}`")

        # -------------------------------------------------------------
        # TAB 4: COLLAB MATCHES & BIO HUBS
        # -------------------------------------------------------------
        with tab_collabs:
            st.markdown("### 🤝 Peer Collaborations & Cross-Platform Recon")

            st.markdown("#### 👥 5 Niche-Matched Peer Collaboration Opportunities")
            collabs = data.get("collab_suggestions", [])
            if collabs:
                for c in collabs:
                    with st.container():
                        co1, co2 = st.columns([3, 1])
                        with co1:
                            st.markdown(f"##### {c['name']} (@{c['handle']})")
                            st.write(f"**Tier:** `{c['tier']}` • **Strategy:** {c['strategy']}")
                            st.write(f"• **Recommended Format:** `{c['format']}`")
                        with co2:
                            st.metric("Niche Match", f"{c['match_score']}%")
                            st.markdown(f"[🔗 Instagram Profile]({c['profile_url']})")
                        st.markdown("---")

            st.markdown("---")
            b_c1, b_c2 = st.columns(2)
            with b_c1:
                st.markdown("#### 🔗 Creator Bio Hubs & Landing Pages")
                bio_links = data.get("bio_links", [])
                if bio_links:
                    for bl in bio_links:
                        st.success(f"🟢 **{bl['name']}:** [{bl['url']}]({bl['url']})")
                else:
                    st.info("⚪ No external bio landing hubs detected under this username.")
            
            with b_c2:
                st.markdown("#### 🌐 Cross-Platform OSINT Correlation")
                cp_list = data.get("cross_platform", [])
                if cp_list:
                    df_cp = pd.DataFrame(cp_list)
                    df_cp["Status"] = df_cp["exists"].apply(lambda x: "🟢 Active / Found" if x else "⚪ Not Found")
                    df_cp = df_cp[["name", "Status", "url"]].rename(columns={"name": "Platform", "url": "URL"})
                    st.dataframe(df_cp, use_container_width=True, hide_index=True)

        # -------------------------------------------------------------
        # TAB 5: 100+ CHECKPOINT AUDIT LOG
        # -------------------------------------------------------------
        with tab_audit:
            st.markdown("### 📋 Complete 100+ Checkpoint Technical & Commercial Audit Log")
            
            categories = data.get("categories", {})
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
