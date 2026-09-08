import streamlit as st
import streamlit.components.v1 as components
from core.ai_synthesizer import AISynthesizer
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="AISynthesizer | Puter.js GPT-5", page_icon="🤖", layout="wide")
st.title("🤖 AISynthesizer: Autonomous AI Script Studio (Puter.js GPT-5 / GPT-4o)")
st.caption("Zero-key browser-based AI synthesis. Synthesizes full 6-hook video scripts grounded in live OSINT data.")

with st.sidebar:
    st.header("🤖 Synthesis Target")
    topic = st.text_input("Target Niche:", value="SaaS AI Marketing")
    country = st.selectbox("Region:", ["US", "IN", "GB", "CA", "AU"], index=0)
    persona = st.selectbox("Creator Persona:", ["tech_educator", "saas_b2b_founder", "finance_real_estate", "fitness_health_coach"], index=0)
    gen_btn = st.button("🚀 Launch AI Synthesizer", type="primary", use_container_width=True)

syn = AISynthesizer()
dummy_seo = {"seed": topic, "commercial": [f"best {topic} tools", f"buy {topic} software", f"{topic} automation"], "pincode_localized_queries": []}
dummy_vids = {"videos": [{"title": f"Why {topic} is changing forever", "vph": 1420, "hook": "The Fortune Teller"}], "hook_dominance": {"The Contrarian": {"percentage": 42.5}, "The Insider": {"percentage": 30.0}}}
dummy_social = {"pain_points": [{"title": f"Too complicated to set up {topic}"}]}

prompt = syn.build_master_dossier_prompt(dummy_seo, dummy_vids, dummy_social, creator_type=persona, country=country)
html_client = syn.generate_puter_html_client(prompt, target_name=topic)

components.html(html_client, height=750, scrolling=True)
