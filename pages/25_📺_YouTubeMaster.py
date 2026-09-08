import pandas as pd
import streamlit as st

from core.youtube_seo_engine import YouTubeMasterEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

st.set_page_config(page_title="YouTubeMaster | SEO Audit", page_icon="📺", layout="wide")
st.title("📺 YouTubeMaster: Channel & Video SEO Audit")
st.caption("100+ checkpoint public-surface audit across branding, CTR, discoverability, retention, and monetization")

with st.sidebar:
    st.header("🎯 Target Investigation")
    target = st.text_input("YouTube Handle or URL", "@mkbhd", placeholder="@mkbhd or channel URL")
    run_audit = st.button("🚀 Run 100+ Point Audit", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("**Audit scope**\n\n- 7 SEO and commercial pillars\n- Same-niche creator matches\n- YouTube autocomplete opportunities\n- Executive PDF export")

if run_audit or "yt_data" not in st.session_state:
    with st.spinner(f"Auditing {target} across public YouTube surfaces..."):
        st.session_state.yt_data = YouTubeMasterEngine().audit_channel(target)

data = st.session_state.yt_data
if data.get("error"):
    st.error(data["error"])
else:
    if data.get("banner_url"):
        st.image(data["banner_url"], use_container_width=True)
    header, score, export = st.columns([5, 2, 2])
    with header:
        st.subheader(f"{data['channel_title']} (@{data['handle']})")
        st.write(f"🏷️ {data['niche']}  ·  🌍 {data.get('country', 'Global')}")
        st.markdown(f"[Open YouTube Channel]({data['channel_url']})")
    with score:
        st.metric("Overall Score", f"{data['overall_score']}%", data["overall_grade"])
        st.metric("Checks Passed", f"{data['passed_checks']} / {data['total_checks']}")
    with export:
        if HAS_PDF:
            pdf = PDFReportGenerator().generate_youtube_pdf(data)
            st.download_button("📄 Download Audit PDF", pdf, f"{data['handle']}_youtube_audit.pdf", "application/pdf", use_container_width=True)

    st.markdown("---")
    metrics = st.columns(4)
    metrics[0].metric("Subscribers", data.get("subscribers_str", "N/A"))
    metrics[1].metric("Total Views", data.get("views_str", "N/A"))
    metrics[2].metric("Published Videos", data.get("videos_str", "N/A"))
    average = int(data["total_views"] / data["video_count"]) if data.get("total_views") and data.get("video_count") else 0
    metrics[3].metric("Average Views / Video", f"{average:,}" if average else "N/A")

    st.subheader("📈 View Traffic & Velocity Forensics")
    st.caption("Modeled public-surface estimates. Exact traffic sources require YouTube Studio analytics access.")
    traffic = data.get("view_traffic", {})
    velocity = st.columns(4)
    velocity[0].metric("7-Day Views", traffic.get("views_7d_str", "N/A"), "Weekly run-rate")
    velocity[1].metric("30-Day Views", traffic.get("views_30d_str", "N/A"), "Monthly volume")
    velocity[2].metric("Daily Run-Rate", traffic.get("daily_views_str", "N/A"))
    velocity[3].metric("Hourly VPH", traffic.get("vph_str", "N/A"), "Views per hour")
    source_col, forecast_col = st.columns([3, 2])
    with source_col:
        st.markdown("#### 🧭 Traffic Acquisition Sources")
        for source, percentage in traffic.get("traffic_sources", {}).items():
            st.write(f"**{source}**: {percentage}%")
            st.progress(percentage / 100)
    with forecast_col:
        st.markdown("#### ⚡ Algorithmic Liquidity")
        st.info(traffic.get("momentum_status", "N/A"))
        st.metric("Views / Subscriber", f"{traffic.get('liquidity_ratio', 0)}x")
        st.write(f"90-day forecast: **{traffic.get('projected_90d', 'N/A')}**")
        st.write(f"1-year forecast: **{traffic.get('projected_annual', 'N/A')}**")

    st.subheader("💰 Commercial Rate Card")
    rates = data["commercial_rates"]
    rate_cols = st.columns(4)
    rate_cols[0].metric("Dedicated Video", f"${rates['dedicated_video_low']:,}-${rates['dedicated_video_high']:,}")
    rate_cols[1].metric("60s Mid-Roll", f"${rates['midroll_integration']:,}")
    rate_cols[2].metric("YouTube Short", f"${rates['short_integration']:,}")
    rate_cols[3].metric("Annual Deal Potential", f"${rates['annual_deal_potential']:,}")

    st.subheader("🤝 Same-Niche Creator Matches")
    collab_df = pd.DataFrame(data["collab_suggestions"])
    if not collab_df.empty:
        st.dataframe(collab_df[["name", "handle", "subscribers", "match_score", "strategy", "format"]].rename(columns={"name": "Creator", "handle": "Handle", "subscribers": "Audience", "match_score": "Match %", "strategy": "Strategy", "format": "Format"}), use_container_width=True, hide_index=True)

    st.subheader("⚡ YouTube Autocomplete Opportunities")
    keywords = pd.DataFrame(data["keyword_opportunities"])
    if not keywords.empty:
        st.dataframe(keywords.rename(columns={"keyword": "Search Term", "type": "Intent", "source": "Source"}), use_container_width=True, hide_index=True)
    else:
        st.info("No autocomplete suggestions were returned.")

    st.subheader("🏛️ Pillar Scorecard")
    for category, values in data["categories"].items():
        st.write(f"**{category}** · {values['grade']} ({values['passed']}/{values['total']})")
        st.progress(values["pct"] / 100)

    st.subheader("⚡ Optimization Roadmap")
    for recommendation in data["recommendations"]:
        st.warning(f"**[{recommendation['priority']}] {recommendation['title']}:** {recommendation['recommendation']}")

    st.subheader("📋 Complete Audit Log")
    st.dataframe(pd.DataFrame(data["checkpoints"])[["id", "category", "name", "status", "detail"]], use_container_width=True, hide_index=True)
