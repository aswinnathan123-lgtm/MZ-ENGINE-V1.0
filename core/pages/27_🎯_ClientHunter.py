import streamlit as st
import pandas as pd
from core.client_hunter_engine import ClientHunterEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(
    page_title="ClientHunter | Agency B2B Client Acquisition Radar",
    page_icon="🎯",
    layout="wide"
)

# Custom Enterprise Styling
st.markdown("""
<style>
    .client-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .badge-hot {
        background: #dc2626;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-high {
        background: #ea580c;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-growth {
        background: #16a34a;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    .pitch-box {
        background: #0f172a;
        border-left: 4px solid #38bdf8;
        padding: 14px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 13px;
        white-space: pre-wrap;
    }
    .schema-box {
        background: #090d16;
        border: 1px solid #1e293b;
        padding: 12px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 12px;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 ClientHunter: Digital Partner Client Acquisition Radar")
st.caption("Find High-Paying Local Clients in ANY Pincode • Website Creation Deals • GBP Optimization • Programmatic SEO Sitemaps • Viral RTN Video Content • Zero API Keys")

with st.sidebar:
    st.header("🎯 Target Client Hunting")
    niche_input = st.selectbox(
        "Target Business Niche:",
        [
            "Dental Clinic",
            "Real Estate & Builders",
            "Gym & Fitness Centers",
            "Interior Designers",
            "Restaurants & Cafes",
            "Chartered Accountants (CA)",
            "Lawyers & Legal Consultants",
            "Salons, Spa & Beauty",
            "Boutiques & Fashion",
            "Coaching & Tuition Centers"
        ]
    )
    loc_input = st.text_input(
        "Target Locality / Pincode / City:",
        value="T Nagar, Chennai (600017)",
        placeholder="e.g. T Nagar Chennai 600017, HSR Layout Bengaluru 560102, Bandra West Mumbai"
    )
    
    run_btn = st.button("🚀 Find & Audit Prospective Clients", type="primary", use_container_width=True)
    st.markdown("---")
    st.markdown("""
    **What This Generates For Your Agency:**
    - 🔍 **Audited Local Business Leads** (No website / Weak GBP)
    - 📍 **High-Intent GBP Keywords** for this exact pincode
    - 🗺️ **Programmatic SEO XML Sitemap** & LocalBusiness Schema
    - 🎬 **RTN Video Script Blueprints** & Trending Locality Hooks
    - 💬 **1-Click WhatsApp, Email & Walk-in Pitches**
    """)

if run_btn or "client_data" not in st.session_state:
    with st.spinner(f"Hunting for high-value client opportunities in '{loc_input}' for '{niche_input}'..."):
        engine = ClientHunterEngine()
        data = engine.scan_locality_clients(niche_input, loc_input)
        st.session_state["client_data"] = data

if "client_data" in st.session_state:
    data = st.session_state["client_data"]

    # -------------------------------------------------------------
    # 1. EXECUTIVE METRICS
    # -------------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Prospective Clients Audited", data["total_leads_found"], f"{data['niche']}")
    m2.metric("🔥 Hot Deals (No Website / Broken)", data["hot_leads_count"], "Highest Conversion Chance")
    m3.metric("Est. Pipeline Deal Value", "₹1,85,000 - ₹3,40,000", "Combined Deal Potential")
    
    with m4:
        st.write("")
        if HAS_PDF:
            pdf_gen = PDFReportGenerator()
            pdf_bytes = pdf_gen.generate_client_hunter_pdf(data)
            if pdf_bytes:
                st.download_button(
                    "📄 Download Agency Proposal PDF",
                    pdf_bytes,
                    file_name=f"{data['niche'].replace(' ', '_')}_{data['location']}_Client_Dossier.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )

    st.markdown("---")

    # -------------------------------------------------------------
    # 2. AUDITED CLIENT PROSPECTS LIST
    # -------------------------------------------------------------
    st.subheader(f"🏢 High-Priority Prospective Clients in {data['location']}")
    st.caption("Detailed diagnostics on Website, Google Business Profile (GBP), SEO, and Local Video Content.")

    for lead in data.get("leads", []):
        badge_cls = "badge-hot" if "HOT" in lead["lead_priority"] else ("badge-high" if "HIGH" in lead["lead_priority"] else "badge-growth")
        st.markdown(f"""
        <div class="client-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin: 0 0 6px 0; color: #f8fafc;">#{lead['id']} {lead['business_name']}</h3>
                    <span style="color: #38bdf8; font-size: 14px;">📍 {lead['location']} • <b>Niche:</b> {lead['niche']}</span>
                </div>
                <div style="text-align: right;">
                    <span class="{badge_cls}">{lead['lead_priority']}</span>
                    <div style="margin-top: 6px; color: #4ade80; font-weight: bold; font-size: 15px;">Est. Deal: {lead['est_deal_value']}</div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin: 14px 0;">
                <div style="background: #0f172a; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <span style="color: #94a3b8; font-size: 11px;">WEBSITE STATUS</span>
                    <div style="color: #cbd5e1; font-size: 13px; font-weight: 500; margin-top: 4px;">{lead['web_status']}</div>
                </div>
                <div style="background: #0f172a; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <span style="color: #94a3b8; font-size: 11px;">GBP (GOOGLE PROFILE)</span>
                    <div style="color: #cbd5e1; font-size: 13px; font-weight: 500; margin-top: 4px;">{lead['gbp_status']}</div>
                </div>
                <div style="background: #0f172a; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <span style="color: #94a3b8; font-size: 11px;">SEO & SITEMAP</span>
                    <div style="color: #cbd5e1; font-size: 13px; font-weight: 500; margin-top: 4px;">{lead['seo_status']}</div>
                </div>
                <div style="background: #0f172a; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <span style="color: #94a3b8; font-size: 11px;">VIDEO CONTENT</span>
                    <div style="color: #cbd5e1; font-size: 13px; font-weight: 500; margin-top: 4px;">{lead['content_status']}</div>
                </div>
            </div>

            <div style="background: #0284c715; border-left: 3px solid #0284c7; padding: 8px 12px; border-radius: 4px; font-size: 13px; color: #38bdf8;">
                💡 <b>Recommended Pitch:</b> {lead['pitch_angle']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------
    # 3. GBP KEYWORDS & PROGRAMMATIC SEO BLUEPRINT
    # -------------------------------------------------------------
    tab_kw, tab_pseo, tab_content, tab_pitch = st.tabs([
        "📍 GBP High-Intent Keywords",
        "🗺️ Programmatic SEO & XML Sitemaps",
        "🎬 Locality RTN Video & Content Pack",
        "💬 1-Click Client Outreach Scripts"
    ])

    with tab_kw:
        st.subheader(f"📍 High-Intent Google Business Profile (GBP) Keywords: {data['location']}")
        st.caption("Top search queries typed by local customers in this specific locality/pincode. Add these to your client's GBP categories, descriptions, and updates.")
        df_kw = pd.DataFrame(data.get("gbp_keywords", []))
        df_kw = df_kw.rename(columns={
            "keyword": "Customer Search Term",
            "intent": "Intent Archetype",
            "search_vol": "Local Demand Volume",
            "cpc_est": "Est. Google Ads Value (CPC)"
        })
        st.dataframe(df_kw, use_container_width=True, hide_index=True)

    with tab_pseo:
        st.subheader("🗺️ Programmatic SEO & Local XML Page Structure")
        st.caption("Deploy these automated location/service landing pages to rank your client on Google across neighboring pincodes.")
        pseo = data.get("pseo_blueprint", {})
        
        st.markdown("#### 📄 Recommended XML Landing Page Slugs")
        for slug in pseo.get("xml_url_slugs", []):
            st.code(slug, language="http")

        st.markdown("#### 🏷️ LocalBusiness JSON-LD Schema Template (Ready for Client Website)")
        st.markdown(f'<div class="schema-box">{pseo.get("schema_markup", "")}</div>', unsafe_allow_html=True)

    with tab_content:
        st.subheader("🎬 Local Content Creation Pack (RTN Videos, Trending Hooks & Pacing)")
        st.caption("Battle-tested viral content formulas designed to capture local Instagram Reels and YouTube Shorts traffic.")
        c_pack = data.get("content_pack", {})
        
        st.markdown("#### 🪝 5 High-Retention (RTN) Locality Video Hooks")
        for h in c_pack.get("hooks", []):
            st.warning(f"**Hook:** {h}")

        st.markdown("#### 🎵 Audio Pacing & Kinetic Visual Formula")
        st.info(c_pack.get("audio_pacing_formula", ""))

        st.markdown("#### 📝 Local Geo-Targeted Caption Template")
        st.markdown(f'<div class="pitch-box">{c_pack.get("caption", "")}</div>', unsafe_allow_html=True)

    with tab_pitch:
        st.subheader("💬 1-Click High-Converting Client Pitch Scripts")
        st.caption("Send these proven direct messages to local business owners to secure website and SEO contracts.")
        pitches = data.get("pitches", {})

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.markdown("#### 📱 High-Response WhatsApp / Instagram DM")
            st.markdown(f'<div class="pitch-box">{pitches.get("whatsapp_dm", "")}</div>', unsafe_allow_html=True)

            st.markdown("#### 🚶 In-Person Walk-in / Phone Opener Script")
            st.markdown(f'<div class="pitch-box">{pitches.get("walkin_script", "")}</div>', unsafe_allow_html=True)

        with p_col2:
            st.markdown("#### ✉️ Executive Client Acquisition Cold Email")
            st.markdown(f'<div class="pitch-box">{pitches.get("cold_email", "")}</div>', unsafe_allow_html=True)
