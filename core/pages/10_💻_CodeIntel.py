import streamlit as st
import pandas as pd
from core.code_intel_engine import CodeIntelEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="CodeIntel | GitHub Repo & Tech Stack", page_icon="💻", layout="wide")
st.title("💻 CodeIntel: GitHub Repository & Language Intelligence")
st.caption("Audit any public GitHub repository: language distribution, commit velocity, stars, and open issues.")

POPULAR_REPOS = ["streamlit/streamlit", "astral-sh/uv", "golang/go", "torvalds/linux", "facebook/react", "rust-lang/rust"]

with st.sidebar:
    st.header("💻 Repository Selection")
    repo_sel = st.selectbox("Popular Repositories:", POPULAR_REPOS, index=0)
    custom_repo = st.text_input("Or Enter Custom Repo:", value="", placeholder="e.g. owner/repo or full github.com URL")
    active_repo = custom_repo.strip() if custom_repo else repo_sel
    run_btn = st.button("🚀 Analyze Repository", type="primary", use_container_width=True)

if run_btn or "code_intel_data" not in st.session_state:
    with st.spinner(f"Analyzing GitHub repo {active_repo}..."):
        engine = CodeIntelEngine()
        data = engine.analyze_repo(active_repo)
        st.session_state["code_intel_data"] = data
        st.session_state["code_intel_active"] = active_repo

if "code_intel_data" in st.session_state:
    data = st.session_state["code_intel_data"]
    if "error" in data:
        st.error(data["error"])
    else:
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.subheader(f"🐙 {data['full_name']}")
            st.write(data["description"])
        with c2:
            st.metric("Primary Language", data["primary_language"])
        with c3:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_code_intel_pdf(data["full_name"], data)
                if pdf_bytes:
                    st.download_button("📄 Export CodeIntel PDF", pdf_bytes, f"{data['repo']}_CodeIntel.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("⭐ Stars", f"{data['stars']:,}")
        with m2: st.metric("🍴 Forks", f"{data['forks']:,}")
        with m3: st.metric("⚠️ Open Issues", f"{data['open_issues']:,}")
        with m4: st.metric("📜 License", data["license"][:20])

        st.markdown("---")
        col_l, col_c = st.columns(2)
        with col_l:
            st.markdown("#### 📊 Programming Languages Byte Distribution")
            langs = data.get("languages", [])
            if langs:
                df_l = pd.DataFrame(langs)
                st.dataframe(df_l[["language", "size_formatted", "percentage"]], use_container_width=True, hide_index=True)
                st.bar_chart(df_l.set_index("language")["percentage"])
            else:
                st.info("No code language breakdown available.")

        with col_c:
            st.markdown("#### ⚡ Commit Velocity Radar")
            vel = data.get("commit_velocity", {})
            st.info(f"**Velocity Status:** `{vel.get('velocity_status')}`")
            st.write(f"• **Commits (Last 7 Days):** `{vel.get('commits_last_7d')}`")
            st.write(f"• **Commits (Last 30 Days):** `{vel.get('commits_last_30d')}`")
            st.markdown("##### 🕒 Recent Commits:")
            for c in vel.get("latest_commits", [])[:5]:
                st.write(f"• `{c['sha']}` **{c['author']}** ({c['date']}): {c['message']}")
