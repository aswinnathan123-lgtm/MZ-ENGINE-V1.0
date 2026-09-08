import urllib.parse
import pandas as pd
import streamlit as st
from core.news_engine import NewsPulseEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(
    page_title="OmniNews | Universal Media Radar & Inshorts Deck",
    page_icon="📰",
    layout="wide"
)

# =====================================================================
# CUSTOM INSHORTS & NEWS STYLING
# =====================================================================
st.markdown(
    """
    <style>
    .inshorts-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    .inshorts-headline {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.35;
        margin-top: 8px;
        margin-bottom: 12px;
    }
    .inshorts-body {
        font-size: 15px;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    .sponsored-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
        border: 2px solid #38bdf8;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.15);
    }
    .tag-badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        background-color: #f1f5f9;
        color: #0284c7;
        margin-right: 6px;
    }
    .virality-chip {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📰 OmniNews: Universal Media Radar, Inshorts & Viral Ad Studio")
st.caption("Zero-key real-time news aggregation across 14+ specialized categories, Inshorts-style 60-word quick cards, viral share velocity, and native client sponsored ad generation.")

# =====================================================================
# 14+ COMPREHENSIVE NEWS CATEGORIES
# =====================================================================
CATEGORIES = {
    "🌍 World Breaking": "WORLD",
    "🇮🇳 India National": "NATION",
    "💻 Technology & Silicon": "TECHNOLOGY",
    "🤖 AI, Robotics & LLMs": "AI",
    "📈 Business, Sensex & Markets": "BUSINESS",
    "🛡️ Defense, Military & Geopolitics": "DEFENSE",
    "🚀 Science & Space Exploration": "SCIENCE",
    "🏥 Health, Pharma & BioTech": "HEALTH",
    "⚡ Clean Energy, EVs & Climate": "ENERGY",
    "🏏 Sports & Cricket Arena": "SPORTS",
    "🎬 Cinema, OTT & Entertainment": "ENTERTAINMENT",
    "🪙 Crypto, Bitcoin & Web3": "CRYPTO",
    "🦄 Startups, VC & Unicorn Deals": "STARTUPS",
    "⚖️ Law, Policy & Governance": "POLICY"
}

# =====================================================================
# SIDEBAR: FILTERS, DEPTH & CLIENT AD SPONSORSHIP SETUP
# =====================================================================
with st.sidebar:
    st.header("📰 News Stream Controls")
    cat_choice = st.selectbox("Select Category:", list(CATEGORIES.keys()), index=0)
    custom_search = st.text_input("Or Search Any Topic / Brand:", value="", placeholder="e.g. Semiconductor, ISRO, Nvidia, Sensex")
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        country_sel = st.selectbox("Country:", ["IN", "US", "GB", "CA", "AU", "SG", "AE"], index=0)
    with col_sb2:
        feed_limit = st.select_slider("News Depth:", options=[15, 25, 40, 50], value=25)

    run_btn = st.button("🚀 Stream News & Viral Radar", type="primary", use_container_width=True)

    st.markdown("---")
    st.header("💼 Client Ad Sponsor Studio")
    st.caption("Insert your client's sponsored native ad directly alongside the most shared viral stories!")
    
    client_name = st.text_input("Client Brand Name:", value="Shri Nithi Infra", placeholder="e.g. Casagrand, Stripe, Your Agency")
    client_product = st.text_input("Client Offer / Product:", value="Premium Luxury Villa Plots with 100% Legal Approval", placeholder="e.g. B2B Payment Infrastructure, Cloud AI")
    client_url = st.text_input("Client Landing URL:", value="https://shrinithiinfra.in", placeholder="https://clientwebsite.com")
    enable_client_ad = st.checkbox("Embed Client Ad in Viral Feed", value=True)

# =====================================================================
# DATA RETRIEVAL & SESSION STATE CACHING
# =====================================================================
cache_key = f"{cat_choice}_{custom_search}_{country_sel}_{feed_limit}"

if run_btn or "omni_news_data" not in st.session_state or st.session_state.get("last_cache_key") != cache_key:
    with st.spinner("Streaming real-time global news feeds & synthesizing Inshorts briefings..."):
        engine = NewsPulseEngine()
        cat_key = CATEGORIES[cat_choice]
        data = engine.fetch_news(
            query=custom_search,
            category=cat_key,
            country=country_sel,
            limit=feed_limit
        )
        st.session_state["omni_news_data"] = data
        st.session_state["last_cache_key"] = cache_key
        st.session_state["card_idx"] = 0

# =====================================================================
# MAIN APPLICATION INTERFACE
# =====================================================================
if "omni_news_data" in st.session_state:
    data = st.session_state["omni_news_data"]
    articles = data.get("articles", [])
    most_shared = data.get("most_shared", [])
    total_found = data.get("total_articles", 0)

    # Top KPI Metrics Header
    h_col1, h_col2, h_col3, h_col4 = st.columns([3, 1, 1, 1])
    with h_col1:
        st.markdown(f"### 📡 Stream: `{data.get('query', 'Headlines')}`")
        st.caption(f"Region: `{data.get('country')}` • Category: `{cat_choice}` • Live Stories: `{total_found}`")
    with h_col2:
        st.metric("Total Stories", total_found)
    with h_col3:
        top_shares = most_shared[0]["virality"]["est_shares"] if most_shared else "0 Shares"
        st.metric("Peak Virality", top_shares)
    with h_col4:
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_news_pdf(data.get("query", "News"), data)
            if pdf_bytes:
                st.download_button(
                    "📄 Export PDF",
                    pdf_bytes,
                    "OmniNews_Intelligence_Report.pdf",
                    "application/pdf",
                    type="primary",
                    use_container_width=True
                )
        else:
            st.caption("PDF Ready")

    st.markdown("---")

    # =================================================================
    # 4 CORE WORKSPACE TABS
    # =================================================================
    tab_inshorts, tab_viral, tab_feed, tab_matrix = st.tabs([
        "⚡ Inshorts 60-Word Deck",
        "🔥 Most Shared & Client Ads",
        "📱 Continuous Short Feed",
        "📊 Media Stream & Sentiment"
    ])

    # -----------------------------------------------------------------
    # TAB 1: INSHORTS 60-WORD DECK (CARD-BY-CARD SWIPE)
    # -----------------------------------------------------------------
    with tab_inshorts:
        st.markdown("### ⚡ Inshorts Quick Deck: 60-Word Micro-Briefings")
        st.caption("Read breaking news in 30 seconds per card. Use the controls below to swipe or navigate through all stories.")

        if articles:
            # Navigation Controls
            card_count = len(articles)
            if "card_idx" not in st.session_state:
                st.session_state["card_idx"] = 0

            # Card navigation row
            n_col1, n_col2, n_col3 = st.columns([1, 2, 1])
            with n_col1:
                if st.button("⬅️ Previous Story", use_container_width=True, disabled=(st.session_state["card_idx"] == 0)):
                    st.session_state["card_idx"] = max(0, st.session_state["card_idx"] - 1)
                    st.rerun()

            with n_col2:
                new_idx = st.slider(
                    "Navigate Stories",
                    min_value=1,
                    max_value=card_count,
                    value=st.session_state["card_idx"] + 1,
                    format="Story %d of " + str(card_count)
                )
                if new_idx - 1 != st.session_state["card_idx"]:
                    st.session_state["card_idx"] = new_idx - 1
                    st.rerun()

            with n_col3:
                if st.button("Next Story ➡️", use_container_width=True, disabled=(st.session_state["card_idx"] >= card_count - 1)):
                    st.session_state["card_idx"] = min(card_count - 1, st.session_state["card_idx"] + 1)
                    st.rerun()

            # Active Card Display
            cur_art = articles[st.session_state["card_idx"]]
            inshorts = cur_art.get("inshorts", {})
            virality = cur_art.get("virality", {})

            sent = cur_art.get("sentiment", "NEUTRAL")
            s_badge = "🟢 BULLISH" if "BULLISH" in sent or "POSITIVE" in sent else ("🔴 BEARISH" if "BEARISH" in sent or "NEGATIVE" in sent else "⚪ NEUTRAL")

            st.markdown(
                f"""
                <div class="inshorts-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <span class="tag-badge">{cur_art.get('tag')}</span>
                            <span class="tag-badge">🕒 {inshorts.get('read_time', '30 sec read')}</span>
                            <span class="tag-badge">{s_badge}</span>
                        </div>
                        <div>
                            <span class="virality-chip" style="background-color: {virality.get('color', '#3b82f6')};">
                                {virality.get('badge')} • {virality.get('score')}/100
                            </span>
                        </div>
                    </div>
                    <div class="inshorts-headline">
                        <a href="{cur_art.get('link')}" target="_blank" style="text-decoration: none; color: #0f172a;">
                            {cur_art.get('title')}
                        </a>
                    </div>
                    <div class="inshorts-body">
                        {inshorts.get('short_text')}
                    </div>
                    <div style="font-size: 13px; color: #64748b; margin-top: 10px; border-top: 1px solid #f1f5f9; padding-top: 10px;">
                        <b>Source:</b> {cur_art.get('source')} • <b>Published:</b> {cur_art.get('pub_date')} • <b>Est. Shares:</b> {virality.get('est_shares')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Key Takeaways Expander
            with st.expander("📌 View 3 Key Takeaways", expanded=True):
                for t in inshorts.get("takeaways", []):
                    st.write(f"• {t}")

            # 1-Click Social Sharing Row
            s_c1, s_c2, s_c3, s_c4 = st.columns(4)
            with s_c1:
                st.markdown(f"<a href='{cur_art.get('whatsapp_link')}' target='_blank'><button style='background-color:#25d366; color:white; border:none; border-radius:6px; padding:7px 14px; cursor:pointer; width:100%; font-weight:600;'>📲 Share on WhatsApp</button></a>", unsafe_allow_html=True)
            with s_c2:
                st.markdown(f"<a href='{cur_art.get('linkedin_link')}' target='_blank'><button style='background-color:#0077b5; color:white; border:none; border-radius:6px; padding:7px 14px; cursor:pointer; width:100%; font-weight:600;'>💼 Share on LinkedIn</button></a>", unsafe_allow_html=True)
            with s_c3:
                st.markdown(f"<a href='{cur_art.get('x_link')}' target='_blank'><button style='background-color:#000000; color:white; border:none; border-radius:6px; padding:7px 14px; cursor:pointer; width:100%; font-weight:600;'>🐦 Share on X (Twitter)</button></a>", unsafe_allow_html=True)
            with s_c4:
                st.markdown(f"<a href='{cur_art.get('link')}' target='_blank'><button style='background-color:#0284c7; color:white; border:none; border-radius:6px; padding:7px 14px; cursor:pointer; width:100%; font-weight:600;'>🔗 Read Full Story</button></a>", unsafe_allow_html=True)
        else:
            st.info("No articles available in this stream.")

    # -----------------------------------------------------------------
    # TAB 2: MOST SHARED NEWS & CLIENT AD SPONSORSHIP RADAR
    # -----------------------------------------------------------------
    with tab_viral:
        st.markdown("### 🔥 Most Shared Viral Stories & Client Native Ad Placement")
        st.caption("Forensic ranking of today's highest-velocity news stories based on headline resonance, publisher tier, and public buzz.")

        engine = NewsPulseEngine()
        top_story_title = most_shared[0]["title"] if most_shared else "Trending Technology and Market Growth"
        ad_hooks = engine.generate_client_ad_hooks(client_name, client_product, client_url, top_story_title)

        # 1. CLIENT SPONSORED NATIVE AD INSERTION
        if enable_client_ad and client_name:
            st.markdown(
                f"""
                <div class="sponsored-banner">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background-color: #38bdf8; color: #0f172a; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">
                            ⭐ SPONSORED TRENDING SPOTLIGHT
                        </span>
                        <span style="font-size: 12px; color: #94a3b8;">Partner Announcement</span>
                    </div>
                    <h3 style="color: #ffffff; margin-top: 6px; margin-bottom: 8px;">
                        {ad_hooks['sponsored_card']['headline']}
                    </h3>
                    <p style="color: #cbd5e1; font-size: 15px; line-height: 1.5; margin-bottom: 14px;">
                        {ad_hooks['sponsored_card']['tagline']} Offering <b>{client_product}</b>.
                    </p>
                    <a href="{client_url}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #38bdf8; color: #0f172a; font-weight: 700; border: none; border-radius: 6px; padding: 8px 18px; cursor: pointer; font-size: 14px;">
                            👉 {ad_hooks['sponsored_card']['cta_text']} ({client_name})
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 2. TOP VIRAL NEWS LIST
        st.markdown("#### 🚀 Top 6 Most Shared & Spreading Stories")
        for rank, item in enumerate(most_shared, 1):
            vir = item.get("virality", {})
            insh = item.get("inshorts", {})
            with st.container():
                v1, v2 = st.columns([3, 1])
                with v1:
                    st.markdown(f"#### #{rank} | [{item.get('title')}]({item.get('link')})")
                    st.write(f"{insh.get('short_text')}")
                    st.caption(f"**Source:** `{item.get('source')}` • **Published:** `{item.get('pub_date')}` • **Tag:** `{item.get('tag')}`")
                with v2:
                    st.metric("Estimated Shares", vir.get("est_shares"))
                    st.markdown(
                        f"""
                        <div style="background-color:{vir.get('color')}; color:white; text-align:center; padding:5px; border-radius:4px; font-weight:700; font-size:12px; margin-top:4px;">
                            {vir.get('badge')} ({vir.get('score')}/100)
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("---")

        # 3. CLIENT AD ANGLE GENERATOR (NEWS-JACKING BLUEPRINTS)
        st.markdown("#### 🎯 Client News-Jacking Ad Angle Generator")
        st.caption(f"Automatically engineered contextual ad hooks connecting **{client_name}** to today's #1 viral headline.")

        for hook in ad_hooks.get("angles", []):
            with st.expander(f"📢 {hook.get('angle_name')}", expanded=True):
                st.write(f"**Hook:** {hook.get('hook')}")
                st.write(f"**Body Copy:** {hook.get('body')}")
                st.code(hook.get("cta"), language="markdown")

        # Ready-to-Send WhatsApp Broadcast Pitch
        with st.expander("📱 Ready-to-Copy WhatsApp Broadcast / Social Ad Copy", expanded=False):
            st.code(ad_hooks.get("whatsapp_broadcast"), language="markdown")

    # -----------------------------------------------------------------
    # TAB 3: CONTINUOUS SHORT FEED (UNLIMITED INSHORTS GRID)
    # -----------------------------------------------------------------
    with tab_feed:
        st.markdown("### 📱 Continuous 60-Word Inshorts Feed")
        st.caption("Scroll through unlimited concise news briefings. Filter by topic tags below.")

        tags = ["All"] + sorted(list(set(a.get("tag") for a in articles if a.get("tag"))))
        selected_tag = st.radio("Filter by Micro-Tag:", tags, horizontal=True)

        filtered_articles = articles if selected_tag == "All" else [a for a in articles if a.get("tag") == selected_tag]

        st.markdown(f"**Displaying {len(filtered_articles)} short stories:**")
        for a in filtered_articles:
            insh = a.get("inshorts", {})
            vir = a.get("virality", {})
            sent = a.get("sentiment", "NEUTRAL")
            s_color = "🟢" if "BULLISH" in sent or "POSITIVE" in sent else ("🔴" if "BEARISH" in sent or "NEGATIVE" in sent else "⚪")

            with st.container():
                st.markdown(f"#### [{a.get('title')}]({a.get('link')})")
                st.write(f"{insh.get('short_text')}")
                st.write(f"**Tag:** `{a.get('tag')}` | **Source:** `{a.get('source')}` | **Sentiment:** {s_color} `{sent}` | **Virality:** `{vir.get('score')}/100` ({vir.get('est_shares')})")
                
                s_share1, s_share2, s_share3 = st.columns([1, 1, 4])
                with s_share1:
                    st.markdown(f"[📲 WhatsApp]({a.get('whatsapp_link')})")
                with s_share2:
                    st.markdown(f"[💼 LinkedIn]({a.get('linkedin_link')})")
                with s_share3:
                    st.markdown(f"[🔗 Original Story]({a.get('link')})")
                st.markdown("---")

    # -----------------------------------------------------------------
    # TAB 4: FULL MEDIA STREAM & SENTIMENT MATRIX
    # -----------------------------------------------------------------
    with tab_matrix:
        st.markdown("### 📊 Media Stream, Sentiment Analysis & Data Table")
        st.caption("Comprehensive data table with one-click export for intelligence reports.")

        s_counts = {"BULLISH / POSITIVE": 0, "BEARISH / NEGATIVE": 0, "NEUTRAL / FACTUAL": 0, "SENSITIVE / WATCH": 0}
        for a in articles:
            s = a.get("sentiment", "NEUTRAL / FACTUAL")
            s_counts[s] = s_counts.get(s, 0) + 1

        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.metric("🟢 Bullish / Positive", s_counts.get("BULLISH / POSITIVE", 0))
        with sc2:
            st.metric("🔴 Bearish / Negative", s_counts.get("BEARISH / NEGATIVE", 0))
        with sc3:
            st.metric("⚠️ Sensitive / Watch", s_counts.get("SENSITIVE / WATCH", 0))
        with sc4:
            st.metric("⚪ Neutral / Factual", s_counts.get("NEUTRAL / FACTUAL", 0))

        st.markdown("---")

        table_rows = []
        for a in articles:
            table_rows.append({
                "Headline": a.get("title"),
                "Source": a.get("source"),
                "Sentiment": a.get("sentiment"),
                "Tag": a.get("tag"),
                "Virality Score": a.get("virality", {}).get("score"),
                "Est Shares": a.get("virality", {}).get("est_shares"),
                "Published": a.get("pub_date")
            })

        if table_rows:
            df_news = pd.DataFrame(table_rows)
            st.dataframe(df_news, use_container_width=True, hide_index=True)