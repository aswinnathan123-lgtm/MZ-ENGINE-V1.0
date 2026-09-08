import streamlit as st

st.set_page_config(
    page_title="NASA OSINT 365 Suite | 23 Intelligence Apps",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .app-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #334155;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .app-card:hover {
        border-color: #38bdf8;
    }
    .app-icon {
        font-size: 26px;
        margin-bottom: 6px;
    }
    .app-title {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .app-desc {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    .badge-pdf {
        background: #dc2626;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛰️ NASA OSINT Intelligence Suite (FAAQ-FINAL-Z)")
st.caption("Microsoft 365 Architecture: 27 Specialized Intelligence Apps • 100% Authentic Zero-Key OSINT • Dedicated PDF Engines")

st.markdown("""
Welcome to the **FAAQ-FINAL-Z Intelligence Suite**. Organized like Microsoft 365 (Word, Excel, PowerPoint, Access), each category is a specialized, independent application with dedicated controls and **executive PDF exports**.

Use the **sidebar on the left** or launch any of the **27 dedicated apps** below:
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📹 Content & Social (6 Apps)",
    "🌐 Web, Infra & Weather (6 Apps)",
    "🛡️ Security & Identity (3 Apps)",
    "📈 Market & Finance (7 Apps)",
    "💻 Code, Patents & AI (4 Apps)"
])

with tab1:
    st.subheader("📹 Content Creation & Social Media Intelligence")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🪝</div><div class="app-title">1. HookStudio</div><div class="app-desc">Live YouTube 6-Hook archetype market share tracker & viral video hook forensic classifier.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/1_🪝_HookStudio.py", label="Open HookStudio", icon="🪝")

        st.markdown('''<div class="app-card"><div><div class="app-icon">⚡</div><div class="app-title">3. VelocityRadar</div><div class="app-desc">Views-Per-Hour (VPH) breakout radar detecting exploding videos in any niche before they peak.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/3_⚡_VelocityRadar.py", label="Open VelocityRadar", icon="⚡")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🎙️</div><div class="app-title">18. PodcastRadar</div><div class="app-desc">Apple Podcasts audio research engine tracking episode volumes, creator feeds, and topics.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/18_🎙️_PodcastRadar.py", label="Open PodcastRadar", icon="🎙️")

        st.markdown('''<div class="app-card"><div><div class="app-icon">📺</div><div class="app-title">25. YouTubeMaster</div><div class="app-desc">100+ point channel and video SEO audit, creator collaboration matches, autocomplete keywords, and sponsorship rate card.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/25_📺_YouTubeMaster.py", label="Open YouTubeMaster", icon="📺")

    with c2:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🎯</div><div class="app-title">2. SearchMatrix</div><div class="app-desc">Google/YouTube real-time 7W1H Question Trees, Commercial Intent, and Local Pincode search expansions.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/2_🎯_SearchMatrix.py", label="Open SearchMatrix", icon="🎯")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🌊</div><div class="app-title">5. PainPointRadar</div><div class="app-desc">Unfiltered customer objections & Reddit discussions mapped to high-retention audio pacing formulas.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/5_🌊_PainPointRadar.py", label="Open PainPointRadar", icon="🌊")

with tab2:
    st.subheader("🌐 Web, Domain, Infrastructure & Weather Recon")
    w1, w2 = st.columns(2)
    with w1:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🌧️</div><div class="app-title">21. WeatherRadar</div><div class="app-desc">Accurate pincode-wise rain probability (%), precipitation sum (mm), and 24h hourly forecast via Open-Meteo ensemble.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/21_🌧️_WeatherRadar.py", label="Open WeatherRadar", icon="🌧️")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🔬</div><div class="app-title">4. DeepAuditor</div><div class="app-desc">Certificate Transparency logs (crt.sh) for subdomains & server tech stack fingerprinting.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/4_🔬_DeepAuditor.py", label="Open DeepAuditor", icon="🔬")

        st.markdown('''<div class="app-card"><div><div class="app-icon">👥</div><div class="app-title">9. TrafficSpy</div><div class="app-desc">SimilarWeb estimated monthly visits, global rank, bounce rate, and acquisition sources.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/9_👥_TrafficSpy.py", label="Open TrafficSpy", icon="👥")

    with w2:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🔍</div><div class="app-title">6. SEOMaster</div><div class="app-desc">On-page technical SEO health score, schema detection, word counts, robots.txt, and sitemap checks.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/6_🔍_SEOMaster.py", label="Open SEOMaster", icon="🔍")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🌐</div><div class="app-title">12. DNSMaster</div><div class="app-desc">Deep DNS resolution (A, AAAA, MX, NS, TXT, SOA) and reverse ASN IP geolocation.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/12_🌐_DNSMaster.py", label="Open DNSMaster", icon="🌐")

        st.markdown('''<div class="app-card"><div><div class="app-icon">⚡</div><div class="app-title">17. SpeedAudit</div><div class="app-desc">Google Lighthouse Core Web Vitals audit: FCP, LCP, CLS, TBT and performance grade.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/17_⚡_SpeedAudit.py", label="Open SpeedAudit", icon="⚡")

with tab3:
    st.subheader("🛡️ Cybersecurity, Identity & Brand OSINT")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🕵️</div><div class="app-title">11. SherlockSocial</div><div class="app-desc">Parallel multi-platform username scanner checking 24+ top social networks for active profiles.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/11_🕵️_SherlockSocial.py", label="Open SherlockSocial", icon="🕵️")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🎨</div><div class="app-title">16. BrandForensics</div><div class="app-desc">Extracts domain brand assets: high-res logos, favicons, brand hex colors, and social footprints.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/16_🎨_BrandForensics.py", label="Open BrandForensics", icon="🎨")

    with s2:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🛡️</div><div class="app-title">13. BreachRadar</div><div class="app-desc">NIST k-anonymity credential exposure check across 800M+ real-world leaked password databases.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/13_🛡️_BreachRadar.py", label="Open BreachRadar", icon="🛡️")

with tab4:
    st.subheader("📈 Financial Markets, Indian vs Foreign Arbitrage")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown('''<div class="app-card"><div><div class="app-icon">⚔️</div><div class="app-title">22. MarketBattle</div><div class="app-desc">Head-to-head investment comparator: Indian Stocks/Indices vs US Stocks with an automated 'Best Buy' verdict.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/22_⚔️_MarketBattle.py", label="Open MarketBattle", icon="⚔️")

        st.markdown('''<div class="app-card"><div><div class="app-icon">📈</div><div class="app-title">7. StockWatcher</div><div class="app-desc">Real-time Yahoo Finance candles, 14-day RSI, 20/50 SMA crossovers, and Buy Probability Scores.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/7_📈_StockWatcher.py", label="Open StockWatcher", icon="📈")

        st.markdown('''<div class="app-card"><div><div class="app-icon">📱</div><div class="app-title">15. AdSpy</div><div class="app-desc">Meta Ad Library & Google Ads Transparency deep-links and competitor creative angle blueprints.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/15_📱_AdSpy.py", label="Open AdSpy", icon="📱")

    with m2:
        st.markdown('''<div class="app-card"><div><div class="app-icon">🪙</div><div class="app-title">8. CryptoWatcher</div><div class="app-desc">Binance real-time spot order book tickers, flash crash dip alerts, and Buy Probability.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/8_🪙_CryptoWatcher.py", label="Open CryptoWatcher", icon="🪙")

        st.markdown('''<div class="app-card"><div><div class="app-icon">💼</div><div class="app-title">19. CompanyIntel</div><div class="app-desc">Corporate registry, executive profiles, Wikipedia verified data, and corporate filings.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/19_💼_CompanyIntel.py", label="Open CompanyIntel", icon="💼")

        st.markdown('''<div class="app-card"><div><div class="app-icon">💼</div><div class="app-title">26. JobRadar</div><div class="app-desc">Naukri and LinkedIn fast-approval job lister, area-wise micro-hubs, response velocity, and recruiter outreach.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/26_💼_JobRadar.py", label="Open JobRadar", icon="💼")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🎯</div><div class="app-title">27. ClientHunter</div><div class="app-desc">B2B client acquisition radar for local website, GBP, SEO, and video opportunities.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/27_🎯_ClientHunter.py", label="Open ClientHunter", icon="🎯")

with tab5:
    st.subheader("💻 Code, Patent R&D & Autonomous AI")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown('''<div class="app-card"><div><div class="app-icon">💡</div><div class="app-title">23. PatentInsider</div><div class="app-desc">Corporate patent surveillance (Google Patents/USPTO) tracking breakthrough stealth R&D by Apple, Tesla, Nvidia, Tata.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/23_💡_PatentInsider.py", label="Open PatentInsider", icon="💡")

        st.markdown('''<div class="app-card"><div><div class="app-icon">💻</div><div class="app-title">10. CodeIntel</div><div class="app-desc">GitHub repository analytics: Python/Go/Rust/TS language distributions, stars, and commit velocity.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/10_💻_CodeIntel.py", label="Open CodeIntel", icon="💻")

    with d2:
        st.markdown('''<div class="app-card"><div><div class="app-icon">📰</div><div class="app-title">14. OmniNews</div><div class="app-desc">Universal news radar covering World, India, Tech & AI, Markets, Defense, and Science with sentiment.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/14_📰_NewsPulse.py", label="Open OmniNews", icon="📰")

        st.markdown('''<div class="app-card"><div><div class="app-icon">🤖</div><div class="app-title">20. AISynthesizer</div><div class="app-desc">Puter.js free GPT-5 / GPT-4o in-browser script generator grounded in real OSINT data.</div></div><div><span class="badge-pdf">📄 PDF Report</span></div></div>''', unsafe_allow_html=True)
        st.page_link("pages/20_🤖_AISynthesizer.py", label="Open AISynthesizer", icon="🤖")

st.markdown("---")
st.caption("NASA OSINT Suite • FAAQ-FINAL-Z Extended Release • Zero Key Architecture • Microsoft 365 Model")
