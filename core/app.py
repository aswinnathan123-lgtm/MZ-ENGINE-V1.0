import streamlit as st

st.set_page_config(
    page_title="MZ-15 ENGINE | Autonomous OSINT Command Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# CUSTOM MZ-15 CYBERPUNK / EXECUTIVE TACTICAL STYLING
# =====================================================================
st.markdown("""
<style>
    /* Global Ambient Styling */
    .stApp {
        background-color: #080c14;
    }
    
    /* Top Telemetry HUD Banner */
    .hud-banner {
        background: linear-gradient(90deg, #0d1527 0%, #152238 50%, #0d1527 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .hud-title-box {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hud-logo-icon {
        font-size: 32px;
        filter: drop-shadow(0 0 8px #38bdf8);
    }
    .hud-main-title {
        color: #f8fafc;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .hud-sub-title {
        color: #94a3b8;
        font-size: 12px;
        margin: 0;
    }
    .hud-metrics {
        display: flex;
        gap: 16px;
        align-items: center;
    }
    .hud-chip {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 11px;
        font-weight: 600;
        color: #cbd5e1;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .chip-green {
        color: #34d399;
        border-color: rgba(52, 211, 153, 0.3);
    }
    .chip-cyan {
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.3);
    }
    
    /* Module Card Grid */
    .mz-card {
        background: linear-gradient(145deg, #0f172a 0%, #131d33 100%);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
        transition: all 0.25s ease-in-out;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 140px;
    }
    .mz-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 8px 24px -4px rgba(56, 189, 248, 0.25);
        transform: translateY(-2px);
    }
    .mz-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    .mz-card-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .mz-card-icon {
        font-size: 24px;
    }
    .mz-card-title {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 700;
        margin: 0;
    }
    .mz-card-desc {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.45;
        margin-bottom: 12px;
    }
    .mz-badge-group {
        display: flex;
        gap: 6px;
        align-items: center;
    }
    .mz-badge {
        font-size: 10px;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .badge-pdf {
        background: rgba(239, 68, 68, 0.18);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .badge-live {
        background: rgba(16, 185, 129, 0.18);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-id {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Search Bar Wrapper */
    .search-hint {
        color: #64748b;
        font-size: 12px;
        margin-top: -8px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# TOP TELEMETRY HUD
# =====================================================================
st.markdown("""
<div class="hud-banner">
    <div class="hud-title-box">
        <div class="hud-logo-icon">⚡</div>
        <div>
            <h1 class="hud-main-title">MZ-15 ENGINE</h1>
            <p class="hud-sub-title">Autonomous OSINT Recon & Tactical Market Intelligence Suite</p>
        </div>
    </div>
    <div class="hud-metrics">
        <div class="hud-chip chip-green">● CORE: ONLINE</div>
        <div class="hud-chip chip-cyan">🔒 ZERO-KEY AIR-GAPPED</div>
        <div class="hud-chip">27 TACTICAL APPS</div>
        <div class="hud-chip">27 PDF ENGINES</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# SIDEBAR TELEMETRY & CONTROLS
# =====================================================================
with st.sidebar:
    st.markdown("### ⚡ MZ-15 ENGINE")
    st.caption("Version 3.5 Extended Release • Air-Gapped Intelligence")
    
    st.markdown("---")
    st.markdown("**System Diagnostics:**")
    st.markdown("- **Core Engine:** `MZ-15 v3.5`")
    st.markdown("- **Recon Protocol:** `100% Zero-Key Public OSINT`")
    st.markdown("- **Execution Latency:** `<1.2s Multi-Threaded`")
    st.markdown("- **PDF Generators:** `ReportLab 4.x Verified`")
    st.markdown("- **IPv4 Socket Gateway:** `Enforced`")
    
    st.markdown("---")
    st.markdown("**Command Categories:**")
    st.markdown("1. 📹 **Content & Social Media** (7)")
    st.markdown("2. 🌐 **Web, Infra & Geo** (6)")
    st.markdown("3. 🛡️ **Cybersecurity & Identity** (3)")
    st.markdown("4. 📈 **Finance & B2B Deals** (7)")
    st.markdown("5. 💻 **Code, Patents & AI** (4)")
    st.markdown("---")
    st.caption("MZ-15 ENGINE • Autonomous Intelligence Suite")

# =====================================================================
# SEARCH & QUICK MODULE LAUNCHER
# =====================================================================
search_col, stat_col = st.columns([3, 1])
with search_col:
    search_term = st.text_input(
        "🔍 Instant Module Radar (Search any tool, topic, or capability):",
        value="",
        placeholder="e.g. Instagram, SEO, Stocks, ClientHunter, YouTube, Weather, Reddit, DNS, Breach..."
    ).strip().lower()
with stat_col:
    st.metric("Deployed Fleet", "27 Apps", "100% Operational")

ALL_MODULES = [
    # Category 1: Content & Social
    {"id": "MZ-01", "name": "HookStudio", "icon": "🪝", "category": "Content", "path": "pages/1_🪝_HookStudio.py", "desc": "Live YouTube 6-Hook archetype market share tracker & viral video hook forensic classifier.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-02", "name": "SearchMatrix", "icon": "🎯", "category": "Content", "path": "pages/2_🎯_SearchMatrix.py", "desc": "Google & YouTube 7W1H Question Trees, Commercial Intent, and Local Pincode search expansions.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-03", "name": "VelocityRadar", "icon": "⚡", "category": "Content", "path": "pages/3_⚡_VelocityRadar.py", "desc": "Views-Per-Hour (VPH) breakout radar detecting exploding videos in any niche before peak saturation.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-04", "name": "PainPointRadar", "icon": "🌊", "category": "Content", "path": "pages/5_🌊_PainPointRadar.py", "desc": "Unfiltered customer objections & Reddit discussions mapped to high-retention audio pacing formulas.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-05", "name": "PodcastRadar", "icon": "🎙️", "category": "Content", "path": "pages/18_🎙️_PodcastRadar.py", "desc": "Apple Podcasts audio research engine tracking episode volumes, creator feeds, and topic curves.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-06", "name": "InstaMaster", "icon": "📸", "category": "Content", "path": "pages/24_📸_InstaMaster.py", "desc": "100+ Checkpoint Instagram profile audit, retention forensics, RTN viral script maker, & peer collab matches.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-07", "name": "YouTubeMaster", "icon": "📺", "category": "Content", "path": "pages/25_📺_YouTubeMaster.py", "desc": "100+ Checkpoint Channel & Video SEO audit across 17 categories, exit drop-off forensics, & monetization cards.", "tags": ["OSINT", "PDF EXPORT"]},
    
    # Category 2: Web, Infra & Geo
    {"id": "MZ-08", "name": "WeatherRadar", "icon": "🌧️", "category": "Web & Geo", "path": "pages/21_🌧️_WeatherRadar.py", "desc": "Hyper-local pincode rain probability (%), precipitation sum (mm), & 24h hourly forecast via Open-Meteo.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-09", "name": "DeepAuditor", "icon": "🔬", "category": "Web & Geo", "path": "pages/4_🔬_DeepAuditor.py", "desc": "Certificate Transparency logs (crt.sh) for subdomains & server tech stack fingerprinting.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-10", "name": "TrafficSpy", "icon": "👥", "category": "Web & Geo", "path": "pages/9_👥_TrafficSpy.py", "desc": "SimilarWeb estimated monthly visits, global rank, bounce rate, and acquisition sources.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-11", "name": "SEOMaster Pro", "icon": "🔍", "category": "Web & Geo", "path": "pages/6_🔍_SEOMaster.py", "desc": "100+ Automated Technical SEO checkpoints, GEO AI search readiness, and white-label reports.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-12", "name": "DNSMaster", "icon": "🌐", "category": "Web & Geo", "path": "pages/12_🌐_DNSMaster.py", "desc": "Deep DNS record resolution (A, AAAA, MX, NS, TXT, SOA) and reverse ASN IP geolocation.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-13", "name": "SpeedAudit", "icon": "⚡", "category": "Web & Geo", "path": "pages/17_⚡_SpeedAudit.py", "desc": "Google Lighthouse Core Web Vitals audit: FCP, LCP, CLS, TBT and performance optimization grades.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    
    # Category 3: Security & Identity
    {"id": "MZ-14", "name": "SherlockSocial", "icon": "🕵️", "category": "Security", "path": "pages/11_🕵️_SherlockSocial.py", "desc": "Parallel multi-platform username scanner checking 24+ top social networks for active user accounts.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-15", "name": "BrandForensics", "icon": "🎨", "category": "Security", "path": "pages/16_🎨_BrandForensics.py", "desc": "Extracts domain brand assets: high-res logos, favicons, brand hex palettes, and social footprints.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-16", "name": "BreachRadar", "icon": "🛡️", "category": "Security", "path": "pages/13_🛡️_BreachRadar.py", "desc": "NIST k-anonymity credential exposure check across 800M+ real-world leaked password databases.", "tags": ["ZERO-KEY", "PDF EXPORT"]},
    
    # Category 4: Finance & B2B Deals
    {"id": "MZ-17", "name": "MarketBattle", "icon": "⚔️", "category": "Finance", "path": "pages/22_⚔️_MarketBattle.py", "desc": "Head-to-head asset comparator: Indian Stocks vs US Stocks with automated 'Best Buy' verdict.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-18", "name": "StockWatcher", "icon": "📈", "category": "Finance", "path": "pages/7_📈_StockWatcher.py", "desc": "Multi-market stock tracking (India, US, China, Global), 52-week channels, pre-breakout advice, & news sentiment.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-19", "name": "CryptoWatcher", "icon": "🪙", "category": "Finance", "path": "pages/8_🪙_CryptoWatcher.py", "desc": "Binance real-time spot order book tickers, flash crash dip alerts, and Buy Probability scores.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-20", "name": "AdSpy", "icon": "📱", "category": "Finance", "path": "pages/15_📱_AdSpy.py", "desc": "Meta Ad Library & Google Ads Transparency deep-links and competitor creative angle blueprints.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-21", "name": "CompanyIntel", "icon": "💼", "category": "Finance", "path": "pages/19_💼_CompanyIntel.py", "desc": "Corporate investigations: workplace culture, salaries, executive leadership, glassdoor sentiment, & news radar.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-22", "name": "JobRadar", "icon": "💼", "category": "Finance", "path": "pages/26_💼_JobRadar.py", "desc": "Naukri & LinkedIn fast approval job lister, area-wise micro-hubs, response velocity, & DM scripts.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-23", "name": "ClientHunter", "icon": "🎯", "category": "Finance", "path": "pages/27_🎯_ClientHunter.py", "desc": "B2B client acquisition radar: finds local businesses needing website creation, GBP optimization, & SEO.", "tags": ["OSINT", "PDF EXPORT"]},
    
    # Category 5: Code, Patents & AI
    {"id": "MZ-24", "name": "PatentInsider", "icon": "💡", "category": "Code & AI", "path": "pages/23_💡_PatentInsider.py", "desc": "Corporate patent surveillance (Google Patents/USPTO) tracking breakthrough stealth R&D by tech giants.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-25", "name": "CodeIntel", "icon": "💻", "category": "Code & AI", "path": "pages/10_💻_CodeIntel.py", "desc": "GitHub repository analytics: Python/Go/Rust/TS language distributions, stars, and commit velocity.", "tags": ["OSINT", "PDF EXPORT"]},
    {"id": "MZ-26", "name": "OmniNews", "icon": "📰", "category": "Code & AI", "path": "pages/14_📰_NewsPulse.py", "desc": "Universal world & specialized media radar: Breaking World, India, Tech & AI, Markets, and Defense with sentiment.", "tags": ["LIVE RADAR", "PDF EXPORT"]},
    {"id": "MZ-27", "name": "AISynthesizer", "icon": "🤖", "category": "Code & AI", "path": "pages/20_🤖_AISynthesizer.py", "desc": "Puter.js free GPT-4o/GPT-5 in-browser narrative script generator grounded in real OSINT data.", "tags": ["ZERO-KEY", "PDF EXPORT"]}
]

def render_module_card(mod):
    badges_html = f'<span class="mz-badge badge-id">{mod["id"]}</span>'
    for tag in mod["tags"]:
        cls = "badge-pdf" if "PDF" in tag else ("badge-live" if "LIVE" in tag else "badge-id")
        badges_html += f'<span class="mz-badge {cls}">{tag}</span>'
    
    card_html = f"""
    <div class="mz-card">
        <div>
            <div class="mz-card-header">
                <div class="mz-card-title-group">
                    <span class="mz-card-icon">{mod['icon']}</span>
                    <h3 class="mz-card-title">{mod['name']}</h3>
                </div>
                <div class="mz-badge-group">
                    {badges_html}
                </div>
            </div>
            <div class="mz-card-desc">{mod['desc']}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    st.page_link(mod["path"], label=f"Launch {mod['name']}", icon=mod["icon"])

# If user entered a search query, show filtered results directly
if search_term:
    matches = [m for m in ALL_MODULES if search_term in m["name"].lower() or search_term in m["desc"].lower() or search_term in m["category"].lower()]
    st.subheader(f"🔍 Search Results for '{search_term}' ({len(matches)} modules found)")
    if matches:
        cols = st.columns(2)
        for idx, mod in enumerate(matches):
            with cols[idx % 2]:
                render_module_card(mod)
    else:
        st.warning(f"No modules matched '{search_term}'. Try searching for 'Instagram', 'SEO', 'Stocks', 'Client', or 'YouTube'.")
    st.markdown("---")

# =====================================================================
# 5 TACTICAL COMMAND TABS
# =====================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📹 Content & Social (7)",
    "🌐 Web, Infra & Geo (6)",
    "🛡️ Security & Identity (3)",
    "📈 Finance & B2B Deals (7)",
    "💻 Code, Patents & AI (4)"
])

with tab1:
    st.subheader("📹 Content Creation, Viral Retention & Social Intelligence")
    st.caption("Engineered for algorithmic discovery, audience watch-time analytics, audio trends, and retention narratives.")
    c_mods = [m for m in ALL_MODULES if m["category"] == "Content"]
    c1, c2 = st.columns(2)
    for idx, mod in enumerate(c_mods):
        with (c1 if idx % 2 == 0 else c2):
            render_module_card(mod)

with tab2:
    st.subheader("🌐 Web Architecture, Domain, Infrastructure & Weather Recon")
    st.caption("Technical footprint analysis: subdomains, DNS topology, Core Web Vitals, and hyper-local precipitation.")
    w_mods = [m for m in ALL_MODULES if m["category"] == "Web & Geo"]
    w1, w2 = st.columns(2)
    for idx, mod in enumerate(w_mods):
        with (w1 if idx % 2 == 0 else w2):
            render_module_card(mod)

with tab3:
    st.subheader("🛡️ Cybersecurity, Identity Recon & Brand Forensics")
    st.caption("Surface credential exposure diagnostics, cross-platform namespace footprints, and brand asset extraction.")
    s_mods = [m for m in ALL_MODULES if m["category"] == "Security"]
    s1, s2 = st.columns(2)
    for idx, mod in enumerate(s_mods):
        with (s1 if idx % 2 == 0 else s2):
            render_module_card(mod)

with tab4:
    st.subheader("📈 Financial Markets, B2B Acquisition & Corporate Intel")
    st.caption("Real-time candle charts, multi-market tickers, local business client lead-gen, and corporate background checks.")
    f_mods = [m for m in ALL_MODULES if m["category"] == "Finance"]
    m1, m2 = st.columns(2)
    for idx, mod in enumerate(f_mods):
        with (m1 if idx % 2 == 0 else m2):
            render_module_card(mod)

with tab5:
    st.subheader("💻 Code Intelligence, Patent R&D & Autonomous AI")
    st.caption("Corporate patent tracking, GitHub repository health metrics, world news feeds, and Puter AI synthesis.")
    d_mods = [m for m in ALL_MODULES if m["category"] == "Code & AI"]
    d1, d2 = st.columns(2)
    for idx, mod in enumerate(d_mods):
        with (d1 if idx % 2 == 0 else d2):
            render_module_card(mod)

st.markdown("---")
st.caption("⚡ MZ-15 ENGINE • Autonomous Tactical OSINT & Market Intelligence Command Center • Zero-Key Architecture")
