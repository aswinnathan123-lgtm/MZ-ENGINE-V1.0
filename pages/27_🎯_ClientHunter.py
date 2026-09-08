import pandas as pd
import streamlit as st

from core.client_hunter_engine import ClientHunterEngine

try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

st.set_page_config(page_title="ClientHunter | Locality Omni-Scan", page_icon="🎯", layout="wide")
st.title("🎯 ClientHunter: Forensic Bio-Data & Corporate Battle Dossier")
st.caption("Diagnose local digital failure, benchmark corporate threats, and package the recovery opportunity")

with st.sidebar:
    st.header("🎯 Target Client Hunting")
    niche_options = ["🌐 ALL CATEGORIES (Locality Omni-Scan: All Businesses)", *ClientHunterEngine.niche_benchmarks.keys(), "✨ Custom / Type Your Own Niche..."]
    selected = st.selectbox("Business Niche", niche_options, index=0)
    niche = st.text_input("Custom Niche", "Physiotherapy Clinic") if selected.startswith("✨") else selected
    location = st.text_input("Locality / Pincode / City", "Madhanandhapuram")
    run_scan = st.button("🚀 Find & Audit Prospective Clients", type="primary", use_container_width=True)
    st.caption("Prospects come from public directory, search, and map surfaces. Verify details before outreach.")

if run_scan or "client_data" not in st.session_state:
    with st.spinner(f"Scanning {location} for {niche}..."):
        st.session_state.client_data = ClientHunterEngine().scan_locality_clients(niche, location)

data = st.session_state.client_data
leads = data.get("leads", [])

export_rows = [{
    "Lead ID": lead["id"],
    "Business Name": lead["business_name"],
    "Category / Niche": lead["niche"],
    "Location": lead["location"],
    "Website Status": lead["web_status"],
    "Google Profile (GBP)": lead["gbp_status"],
    "Organic SEO Status": lead["seo_status"],
    "Video Content Status": lead["content_status"],
    "Lead Priority": lead["lead_priority"],
    "Est Deal Value (INR)": lead["est_deal_value"],
    "Recommended Site Pages": lead.get("site_pages", ""),
    "Programmatic XML Slugs": lead.get("xml_slugs", ""),
    "Full XML Sitemap Code": lead.get("xml_file_content", ""),
    "JSON-LD Schema Markup": lead.get("schema_json", ""),
    "Recommended Pitch Angle": lead["pitch_angle"],
    "Pre-written WhatsApp Pitch": lead.get("whatsapp_dm", ""),
    "Source": lead.get("source", "Surface Web"),
    "Historical Footprint": lead.get("hist_timeline", ""),
    "Digital Health Score": lead.get("health_score", ""),
    "Corporate Competitor Threat": lead.get("corporate_rival", ""),
    "Where Local Business Fails": lead.get("where_local_fails", ""),
    "Where Corporate Wins": lead.get("where_corp_wins", ""),
    "Estimated Annual Revenue Leak": lead.get("revenue_leak", ""),
} for lead in leads]
export_df = pd.DataFrame(export_rows)

metrics = st.columns(4)
metrics[0].metric("Clients Discovered", data.get("total_leads_found", 0), data.get("location", ""))
metrics[1].metric("🔥 Hot Deals", data.get("hot_leads_count", 0), "No website / high opportunity")
metrics[2].metric("Categories", export_df["Category / Niche"].nunique() if not export_df.empty else 0)
with metrics[3]:
    st.download_button("📥 Download All Clients (.CSV)", export_df.to_csv(index=False).encode("utf-8"), f"{data.get('location', 'locality')}_client_roster.csv", "text/csv", use_container_width=True)

st.download_button("📥 Download Locality Sitemap (.XML)", data.get("master_xml_file", ""), f"{data.get('location', 'locality')}_sitemap.xml", "application/xml")

st.subheader(f"📋 Master Client Roster: {data.get('location', '')}")
category_values = ["All Categories"] + sorted(export_df["Category / Niche"].dropna().unique().tolist()) if not export_df.empty else ["All Categories"]
filter_col, hot_col = st.columns([2, 1])
with filter_col:
    category_filter = st.selectbox("Filter by Category", category_values)
with hot_col:
    hot_only = st.checkbox("🔥 Hot Deals Only", value=False)

displayed = export_df.copy()
if category_filter != "All Categories":
    displayed = displayed[displayed["Category / Niche"] == category_filter]
if hot_only:
    displayed = displayed[displayed["Lead Priority"].str.contains("HOT", na=False)]

if displayed.empty:
    st.warning("No matching real businesses found. Broaden the locality or turn off the hot-leads filter.")
else:
    st.dataframe(displayed[["Lead ID", "Business Name", "Category / Niche", "Location", "Historical Footprint", "Digital Health Score", "Corporate Competitor Threat", "Estimated Annual Revenue Leak", "Website Status", "Lead Priority", "Est Deal Value (INR)", "Source"]], use_container_width=True, hide_index=True)

if HAS_PDF:
    pdf = PDFReportGenerator().generate_client_hunter_pdf(data)
    st.download_button("📄 Download Master Locality Dossier (PDF)", pdf, "clienthunter_master_dossier.pdf", "application/pdf")

st.markdown("---")
st.subheader("🏢 Detailed Prospect Diagnostics")
for lead in leads:
    with st.expander(f"#{lead['id']} {lead['business_name']} · {lead['niche']} · {lead['lead_priority']}"):
        st.write(f"**Source:** {lead.get('source', 'Surface Web')}  |  **Estimated deal:** {lead['est_deal_value']}")
        st.write(f"**Website:** {lead['web_status']}")
        st.write(f"**GBP:** {lead['gbp_status']}")
        st.write(f"**SEO:** {lead['seo_status']}")
        st.write(f"**Video:** {lead['content_status']}")
        st.write(f"**Operating footprint:** {lead.get('hist_timeline', 'N/A')}  |  **Digital health:** {lead.get('health_score', 'N/A')}")
        st.error(f"**Where local businesses fail:** {lead.get('where_local_fails', 'N/A')}\n\n**Estimated annual revenue leak:** {lead.get('revenue_leak', 'N/A')}")
        st.success(f"**Corporate benchmark ({lead.get('corporate_rival', 'N/A')}):** {lead.get('where_corp_wins', 'N/A')}")
        st.info(lead.get("whatsapp_dm", lead["pitch_angle"]))
        st.code(lead.get("xml_slugs", ""), language="text")

st.markdown("---")
tab_keywords, tab_seo, tab_content, tab_pitch = st.tabs(["📍 GBP Keywords", "🗺️ Programmatic SEO", "🎬 Local Content Pack", "💬 Outreach Scripts"])
with tab_keywords:
    st.dataframe(pd.DataFrame(data.get("gbp_keywords", [])), use_container_width=True, hide_index=True)
with tab_seo:
    blueprint = data.get("pseo_blueprint", {})
    for slug in blueprint.get("xml_url_slugs", []):
        st.code(slug, language="text")
    st.code(blueprint.get("schema_markup", ""), language="json")
with tab_content:
    pack = data.get("content_pack", {})
    for hook in pack.get("hooks", []):
        st.warning(hook)
    st.info(pack.get("audio_pacing_formula", ""))
    st.code(pack.get("caption", ""), language="text")
with tab_pitch:
    pitches = data.get("pitches", {})
    st.code(pitches.get("whatsapp_dm", ""), language="text")
    st.code(pitches.get("cold_email", ""), language="text")
    st.code(pitches.get("walkin_script", ""), language="text")
