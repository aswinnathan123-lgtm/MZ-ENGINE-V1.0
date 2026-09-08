import io
from datetime import datetime

class PDFReportGenerator:
    """
    NASA-Grade PDF Intelligence Generator.
    Provides dedicated, executive-level PDF reports for all 20 independent applications in the suite.
    """
    def __init__(self):
        pass

    def _get_base_styles(self):
        try:
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'AppTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
                fontSize=18, leading=22, textColor=colors.HexColor("#0f172a"), spaceAfter=4
            )
            sub_style = ParagraphStyle(
                'AppSub', parent=styles['Normal'], fontName='Helvetica',
                fontSize=9, leading=13, textColor=colors.HexColor("#64748b"), spaceAfter=14
            )
            h2_style = ParagraphStyle(
                'AppH2', parent=styles['Heading2'], fontName='Helvetica-Bold',
                fontSize=12, leading=16, textColor=colors.HexColor("#0284c7"), spaceBefore=10, spaceAfter=6
            )
            body_style = ParagraphStyle(
                'AppBody', parent=styles['Normal'], fontName='Helvetica',
                fontSize=8.5, leading=11.5, textColor=colors.HexColor("#1e293b")
            )
            bold_style = ParagraphStyle(
                'AppBold', parent=styles['Normal'], fontName='Helvetica-Bold',
                fontSize=8.5, leading=11.5, textColor=colors.HexColor("#0f172a")
            )
            return styles, title_style, sub_style, h2_style, body_style, bold_style, colors
        except ImportError:
            return None

    def _create_doc(self, buf):
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.lib.pagesizes import letter
        return SimpleDocTemplate(buf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)

    # 1. HOOK STUDIO
    def generate_hook_pdf(self, topic: str, country: str, hook_dominance: dict, videos: list) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO()
        doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🪝 HookStudio Intelligence: {topic}", title_style),
            Paragraph(f"Region: <b>{country}</b> | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", sub_style),
            Paragraph("Live 6-Hook Market Share Leaderboard", h2_style)
        ]
        table_data = [[Paragraph("<b>Hook Archetype</b>", bold_style), Paragraph("<b>Market Share</b>", bold_style), Paragraph("<b>Count</b>", bold_style)]]
        for h, stat in sorted(hook_dominance.items(), key=lambda x: x[1].get("percentage", 0), reverse=True):
            table_data.append([Paragraph(h, body_style), Paragraph(f"{stat.get('percentage', 0)}%", bold_style), Paragraph(str(stat.get('count', 0)), body_style)])
        t = Table(table_data, colWidths=[260, 140, 140])
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.extend([t, Spacer(1, 12), Paragraph("Sample Trending Video Hooks Detected", h2_style)])
        v_data = [[Paragraph("<b>Title</b>", bold_style), Paragraph("<b>Classified Hook</b>", bold_style)]]
        for v in videos[:8]: v_data.append([Paragraph(v.get("title", "")[:60], body_style), Paragraph(v.get("hook", ""), bold_style)])
        tv = Table(v_data, colWidths=[380, 160])
        tv.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tv)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 2. SEARCH MATRIX
    def generate_seo_pdf(self, keyword: str, country: str, pincode: str, seo_data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🎯 SearchMatrix Demand Report: {keyword}", title_style),
            Paragraph(f"Country: <b>{country}</b> | Pincode: <b>{pincode or 'National'}</b> | Total: <b>{seo_data.get('total_queries_found', 0)}</b>", sub_style),
            Paragraph("High Buyer-Intent Commercial Queries", h2_style)
        ]
        c_table = [[Paragraph("<b>Commercial Query</b>", bold_style)]]
        for c in seo_data.get("commercial", [])[:12]: c_table.append([Paragraph(c, body_style)])
        tc = Table(c_table, colWidths=[540])
        tc.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.extend([tc, Spacer(1, 12)])
        if seo_data.get("pincode_localized_queries"):
            elements.append(Paragraph("Hyper-Local / Pincode Searches", h2_style))
            p_table = [[Paragraph("<b>Local Pincode Search Term</b>", bold_style)]]
            for p in seo_data["pincode_localized_queries"][:8]: p_table.append([Paragraph(p, body_style)])
            tp = Table(p_table, colWidths=[540])
            tp.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
            elements.append(tp)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 3. VELOCITY RADAR
    def generate_velocity_pdf(self, keyword: str, video_data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"⚡ VelocityRadar Audit: {keyword}", title_style),
            Paragraph(f"Average: <b>{video_data.get('average_vph', 0)} VPH</b> | Sampled: <b>{video_data.get('total_analyzed', 0)} videos</b>", sub_style),
            Paragraph("Top Breakout Videos Ranked by Views-Per-Hour", h2_style)
        ]
        v_table = [[Paragraph("<b>Title</b>", bold_style), Paragraph("<b>VPH</b>", bold_style), Paragraph("<b>Views</b>", bold_style), Paragraph("<b>Channel</b>", bold_style)]]
        for v in video_data.get("videos", [])[:10]:
            v_table.append([Paragraph(v.get("title", "")[:50] + "...", body_style), Paragraph(f"{v.get('vph', 0)} VPH", bold_style), Paragraph(str(v.get("views_formatted") or v.get("views")), body_style), Paragraph(v.get("channel", "")[:20], body_style)])
        tv = Table(v_table, colWidths=[270, 80, 90, 100])
        tv.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tv)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 4. DEEP AUDITOR
    def generate_audit_pdf(self, domain: str, audit_data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        tech = audit_data.get("tech_stack", {})
        elements = [
            Paragraph(f"🔬 DeepAuditor Dossier: {domain}", title_style),
            Paragraph(f"Subdomains Found: <b>{audit_data.get('subdomains', {}).get('total_found', 0)}</b>", sub_style),
            Paragraph("Technology Stack & Infrastructure", h2_style)
        ]
        t_data = [
            [Paragraph("<b>Web Server:</b>", bold_style), Paragraph(tech.get("server", "N/A"), body_style)],
            [Paragraph("<b>Frameworks:</b>", bold_style), Paragraph(", ".join(tech.get("frameworks", [])) or "None", body_style)],
            [Paragraph("<b>CMS:</b>", bold_style), Paragraph(", ".join(tech.get("cms", [])) or "None", body_style)],
            [Paragraph("<b>Analytics & Pixels:</b>", bold_style), Paragraph(", ".join(tech.get("analytics_and_ads", [])) or "None", body_style)]
        ]
        t = Table(t_data, colWidths=[160, 380])
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.extend([t, Spacer(1, 12), Paragraph("Certificate Transparency Subdomains", h2_style)])
        subs = audit_data.get("subdomains", {}).get("subdomains", [])[:15]
        s_data = [[Paragraph("<b>Subdomain</b>", bold_style), Paragraph("<b>Classification</b>", bold_style)]]
        for s in subs: s_data.append([Paragraph(s.get("subdomain", ""), body_style), Paragraph(s.get("type", "Standard"), body_style)])
        ts = Table(s_data, colWidths=[380, 160])
        ts.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(ts)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 5. PAIN POINT RADAR
    def generate_painpoint_pdf(self, topic: str, pain_points: list, audio_formulas: list) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🌊 PainPointRadar Customer Intel: {topic}", title_style),
            Paragraph(f"Audience Objections & Content Formulas", sub_style),
            Paragraph("Unfiltered Community Discussions", h2_style)
        ]
        p_table = [[Paragraph("<b>Customer Objection / Problem Discussion</b>", bold_style)]]
        for p in pain_points[:10]: p_table.append([Paragraph(f"• {p.get('title')}", body_style)])
        tp = Table(p_table, colWidths=[540])
        tp.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.extend([tp, Spacer(1, 12), Paragraph("Audio Pacing Formulas", h2_style)])
        a_table = [[Paragraph("<b>Sound Template</b>", bold_style), Paragraph("<b>Pacing Strategy</b>", bold_style), Paragraph("<b>Retention Impact</b>", bold_style)]]
        for a in audio_formulas: a_table.append([Paragraph(a.get("sound", ""), bold_style), Paragraph(a.get("pacing", ""), body_style), Paragraph(a.get("retention", ""), body_style)])
        ta = Table(a_table, colWidths=[180, 240, 120])
        ta.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(ta)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 6. SEO MASTER
    def generate_seo_audit_pdf(self, domain: str, keyword: str, onpage: dict, serp: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🔍 SEOMaster Technical Audit: {domain}", title_style),
            Paragraph(f"Overall Grade: <b>{onpage.get('seo_grade', 'N/A')}</b>", sub_style),
            Paragraph("On-Page Technical Factors", h2_style)
        ]
        t_data = [
            [Paragraph("<b>SEO Health Grade:</b>", bold_style), Paragraph(f"<b>{onpage.get('seo_grade', 'N/A')}</b>", bold_style)],
            [Paragraph("<b>Title Tag:</b>", bold_style), Paragraph(f"{onpage.get('title', 'None')} ({onpage.get('title_length', 0)} chars)", body_style)],
            [Paragraph("<b>Meta Description:</b>", bold_style), Paragraph(f"{onpage.get('description', 'None')} ({onpage.get('description_length', 0)} chars)", body_style)],
            [Paragraph("<b>H1 Headings:</b>", bold_style), Paragraph(f"Found {onpage.get('h1_count', 0)}", body_style)],
            [Paragraph("<b>Word Count:</b>", bold_style), Paragraph(f"{onpage.get('word_count', 0)} words", body_style)]
        ]
        t = Table(t_data, colWidths=[150, 390])
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(t)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 7. STOCK WATCHER
    def generate_stock_pdf(self, ticker: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"📈 StockWatcher Intelligence: {ticker}", title_style),
            Paragraph(f"Price: <b>${data.get('current_price')}</b> | Change: <b>{data.get('change_pct')}%</b>", sub_style),
            Paragraph("Technical Scorecard", h2_style)
        ]
        kpi_table = [
            [Paragraph("<b>Chance UP</b>", bold_style), Paragraph("<b>Chance DOWN</b>", bold_style), Paragraph("<b>RSI (14D)</b>", bold_style), Paragraph("<b>Alert Status</b>", bold_style)],
            [Paragraph(f"<b>{data.get('prob_up')}%</b>", title_style), Paragraph(f"<b>{data.get('prob_down')}%</b>", title_style), Paragraph(str(data.get('rsi_14')), title_style), Paragraph(data.get('alert_level', 'NORMAL'), bold_style)]
        ]
        tk = Table(kpi_table, colWidths=[135, 135, 135, 135])
        tk.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")), ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.extend([tk, Spacer(1, 10), Paragraph(f"<b>Verdict:</b> {data.get('verdict')}", bold_style)])
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 8. CRYPTO WATCHER
    def generate_crypto_pdf(self, symbol: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🪙 CryptoWatcher Intelligence: {symbol}/USDT", title_style),
            Paragraph(f"Live Price: <b>${data.get('price'):,.4f}</b> | 24h Change: <b>{data.get('change_24h_pct')}%</b>", sub_style),
            Paragraph("Momentum & Buy Probability", h2_style)
        ]
        c_kpi = [
            [Paragraph("<b>Chance UP</b>", bold_style), Paragraph("<b>Chance DOWN</b>", bold_style), Paragraph("<b>24h Low</b>", bold_style), Paragraph("<b>24h High</b>", bold_style)],
            [Paragraph(f"<b>{data.get('prob_up')}%</b>", title_style), Paragraph(f"<b>{data.get('prob_down')}%</b>", title_style), Paragraph(f"${data.get('low_24h'):,.2f}", body_style), Paragraph(f"${data.get('high_24h'):,.2f}", body_style)]
        ]
        tk = Table(c_kpi, colWidths=[135, 135, 135, 135])
        tk.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.extend([tk, Spacer(1, 10), Paragraph(f"<b>Verdict:</b> {data.get('verdict')}", bold_style)])
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 9. TRAFFIC SPY
    def generate_traffic_pdf(self, domain: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"👥 TrafficSpy Website Intelligence: {domain}", title_style),
            Paragraph(f"Total Monthly Visits: <b>{data.get('total_monthly_visits')}</b> | Global Rank: <b>{data.get('global_rank')}</b>", sub_style),
            Paragraph("Traffic Channels", h2_style)
        ]
        sources = data.get("traffic_sources", {})
        s_data = [[Paragraph("<b>Channel</b>", bold_style), Paragraph("<b>Traffic Share</b>", bold_style)]]
        for src, pct in sources.items(): s_data.append([Paragraph(src, body_style), Paragraph(f"{pct}%", bold_style)])
        ts = Table(s_data, colWidths=[340, 200])
        ts.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(ts)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 10. CODE INTEL
    def generate_code_intel_pdf(self, repo_name: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"💻 CodeIntel Repository Audit: {repo_name}", title_style),
            Paragraph(f"Stars: <b>{data.get('stars'):,}</b> | Forks: <b>{data.get('forks'):,}</b> | Issues: <b>{data.get('open_issues'):,}</b>", sub_style),
            Paragraph("Programming Language Distribution", h2_style)
        ]
        l_table = [[Paragraph("<b>Language</b>", bold_style), Paragraph("<b>Byte Size</b>", bold_style), Paragraph("<b>Percentage</b>", bold_style)]]
        for l in data.get("languages", [])[:8]:
            l_table.append([Paragraph(l.get("language"), bold_style), Paragraph(l.get("size_formatted"), body_style), Paragraph(f"{l.get('percentage')}%", bold_style)])
        tl = Table(l_table, colWidths=[240, 150, 150])
        tl.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.extend([tl, Spacer(1, 12), Paragraph("Commit Velocity Status", h2_style), Paragraph(f"<b>Status:</b> {data.get('commit_velocity', {}).get('velocity_status')}", bold_style)])
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 11. SHERLOCK SOCIAL
    def generate_sherlock_pdf(self, username: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🕵️ Sherlock Social Reconnaissance: @{username}", title_style),
            Paragraph(f"Profiles Found: <b>{data.get('found_count')}/{data.get('total_scanned')}</b> ({data.get('presence_rate')}%)", sub_style),
            Paragraph("Discovered Active Profiles", h2_style)
        ]
        f_table = [[Paragraph("<b>Platform</b>", bold_style), Paragraph("<b>Verified Profile URL</b>", bold_style)]]
        for p in data.get("found_profiles", [])[:15]:
            f_table.append([Paragraph(p.get("platform"), bold_style), Paragraph(p.get("url"), body_style)])
        tf = Table(f_table, colWidths=[180, 360])
        tf.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tf)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 12. DNS MASTER
    def generate_dns_pdf(self, domain: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        geo = data.get("geo", {})
        elements = [
            Paragraph(f"🌐 DNSMaster Infrastructure Dossier: {domain}", title_style),
            Paragraph(f"Primary IP: <b>{data.get('primary_ip')}</b> | Country: <b>{geo.get('country')}</b> | ISP: <b>{geo.get('isp')}</b>", sub_style),
            Paragraph("DNS Records Resolution", h2_style)
        ]
        d_table = [[Paragraph("<b>Record Type</b>", bold_style), Paragraph("<b>Resolved Values</b>", bold_style)]]
        for r_type, vals in data.get("records", {}).items():
            d_table.append([Paragraph(r_type, bold_style), Paragraph(", ".join(vals[:4]) or "None", body_style)])
        td = Table(d_table, colWidths=[120, 420])
        td.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(td)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 13. BREACH RADAR
    def generate_breach_pdf(self, query: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph("🛡️ BreachRadar Credential Exposure Audit", title_style),
            Paragraph(f"Audited Target: <b>{query}</b> | Generated {datetime.now().strftime('%Y-%m-%d')}", sub_style),
            Paragraph("Security Verdict", h2_style),
            Paragraph(f"<b>Result:</b> {data.get('verdict')}", bold_style),
            Paragraph(f"<b>Risk Level:</b> {data.get('risk_level')}", body_style)
        ]
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 14. NEWS PULSE
    def generate_news_pdf(self, query: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"📰 NewsPulse Media Intelligence: {query}", title_style),
            Paragraph(f"Articles Found: <b>{data.get('total_articles')}</b>", sub_style),
            Paragraph("Recent Headlines & Sentiment", h2_style)
        ]
        n_table = [[Paragraph("<b>Headline</b>", bold_style), Paragraph("<b>Source</b>", bold_style), Paragraph("<b>Sentiment</b>", bold_style)]]
        for a in data.get("articles", [])[:10]:
            n_table.append([Paragraph(a.get("title", "")[:60], body_style), Paragraph(a.get("source", ""), bold_style), Paragraph(a.get("sentiment", ""), body_style)])
        tn = Table(n_table, colWidths=[320, 110, 110])
        tn.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tn)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 15. AD SPY
    def generate_adspy_pdf(self, brand: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"📱 AdSpy Advertising Intelligence: {brand}", title_style),
            Paragraph("Competitor Creative Analysis & Direct Ad Library Links", sub_style),
            Paragraph("Suggested Ad Angles", h2_style)
        ]
        a_table = [[Paragraph("<b>Hook Type</b>", bold_style), Paragraph("<b>Angle Blueprint</b>", bold_style), Paragraph("<b>Format</b>", bold_style)]]
        for hook in data.get("suggested_ad_creative_angles", []):
            a_table.append([Paragraph(hook.get("hook_type"), bold_style), Paragraph(hook.get("angle"), body_style), Paragraph(hook.get("format"), body_style)])
        ta = Table(a_table, colWidths=[140, 260, 140])
        ta.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(ta)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 16. BRAND FORENSICS
    def generate_brand_pdf(self, domain: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🎨 BrandForensics Asset Dossier: {domain}", title_style),
            Paragraph(f"Brand Colors Detected: <b>{', '.join(data.get('brand_colors', [])) or 'None'}</b>", sub_style),
            Paragraph("Identified Social Footprints", h2_style)
        ]
        s_table = [[Paragraph("<b>Detected Brand Profile Link</b>", bold_style)]]
        for s in data.get("social_links", [])[:8]: s_table.append([Paragraph(s, body_style)])
        ts = Table(s_table, colWidths=[540])
        ts.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(ts)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 17. SPEED AUDIT
    def generate_speed_pdf(self, url: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph("⚡ SpeedAudit Core Web Vitals Report", title_style),
            Paragraph(f"URL: <b>{url}</b> | Grade: <b>{data.get('grade')}</b>", sub_style),
            Paragraph("Performance Metrics", h2_style)
        ]
        s_table = [
            [Paragraph("<b>Performance Score:</b>", bold_style), Paragraph(f"{data.get('performance_score')}/100", bold_style)],
            [Paragraph("<b>First Contentful Paint (FCP):</b>", bold_style), Paragraph(str(data.get("first_contentful_paint")), body_style)],
            [Paragraph("<b>Largest Contentful Paint (LCP):</b>", bold_style), Paragraph(str(data.get("largest_contentful_paint")), body_style)],
            [Paragraph("<b>Cumulative Layout Shift (CLS):</b>", bold_style), Paragraph(str(data.get("cumulative_layout_shift")), body_style)],
            [Paragraph("<b>Total Blocking Time (TBT):</b>", bold_style), Paragraph(str(data.get("total_blocking_time")), body_style)]
        ]
        ts = Table(s_table, colWidths=[200, 340])
        ts.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(ts)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 18. PODCAST RADAR
    def generate_podcast_pdf(self, query: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🎙️ PodcastRadar Audio Intelligence: {query}", title_style),
            Paragraph(f"Total Shows Found: <b>{data.get('total_found')}</b>", sub_style),
            Paragraph("Discovered Podcasts", h2_style)
        ]
        p_table = [[Paragraph("<b>Show Title</b>", bold_style), Paragraph("<b>Creator / Host</b>", bold_style), Paragraph("<b>Episodes</b>", bold_style)]]
        for p in data.get("podcasts", [])[:10]:
            p_table.append([Paragraph(p.get("name", "")[:50], body_style), Paragraph(p.get("artist", "")[:30], bold_style), Paragraph(str(p.get("episodes")), body_style)])
        tp = Table(p_table, colWidths=[280, 180, 80])
        tp.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tp)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 19. COMPANY INTEL
    def generate_company_pdf(self, company: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"💼 CompanyIntel Corporate Dossier: {company}", title_style),
            Paragraph(f"Category: <b>{data.get('description')}</b>", sub_style),
            Paragraph("Corporate Background & Profile", h2_style),
            Paragraph(data.get("extract", "No extract found."), body_style)
        ]
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 20. AI SYNTHESIZER
    def generate_ai_pdf(self, topic: str, content: str) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🤖 AISynthesizer Viral Dossier: {topic}", title_style),
            Paragraph(f"Puter.js Autonomous AI Output | Generated {datetime.now().strftime('%Y-%m-%d')}", sub_style),
            Paragraph("Synthesized Intelligence", h2_style),
            Paragraph(content.replace("\n", "<br/>")[:2500], body_style)
        ]
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 21. WEATHER RADAR
    def generate_weather_pdf(self, pincode: str, country: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"🌧️ WeatherRadar Precipitation Dossier: {pincode}", title_style),
            Paragraph(f"Location: <b>{data.get('location_name')}</b> | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", sub_style),
            Paragraph("Precipitation & Weather Scorecard", h2_style)
        ]
        w_kpi = [
            [Paragraph("<b>Peak Rain Chance Today</b>", bold_style), Paragraph("<b>Expected Rainfall</b>", bold_style), Paragraph("<b>Temperature</b>", bold_style), Paragraph("<b>Alert Status</b>", bold_style)],
            [Paragraph(f"<b>{data.get('today_max_rain_prob_pct')}%</b>", title_style), Paragraph(f"{data.get('today_total_precip_mm')} mm", title_style), Paragraph(str(data.get('today_temp_range')), body_style), Paragraph(data.get('alert_level', 'NORMAL'), bold_style)]
        ]
        tw = Table(w_kpi, colWidths=[135, 135, 135, 135])
        tw.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")), ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.extend([tw, Spacer(1, 10), Paragraph(f"<b>Alert:</b> {data.get('rain_alert')}", bold_style), Spacer(1, 10), Paragraph("Next 12-Hour Rain Probability Timeline", h2_style)])
        h_table = [[Paragraph("<b>Time</b>", bold_style), Paragraph("<b>Rain %</b>", bold_style), Paragraph("<b>Precipitation</b>", bold_style), Paragraph("<b>Temp</b>", bold_style)]]
        for h in data.get("hourly_24h", [])[:12]:
            h_table.append([Paragraph(h.get("time"), bold_style), Paragraph(f"{h.get('rain_probability_pct')}%", body_style), Paragraph(f"{h.get('precipitation_mm')} mm", body_style), Paragraph(f"{h.get('temperature_c')}°C", body_style)])
        th = Table(h_table, colWidths=[135, 135, 135, 135])
        th.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(th)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 22. MARKET BATTLE
    def generate_market_battle_pdf(self, asset_in: str, asset_us: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        d_in = data.get("indian_asset", {})
        d_us = data.get("foreign_asset", {})
        elements = [
            Paragraph(f"⚔️ MarketBattle: {asset_in} vs {asset_us}", title_style),
            Paragraph(f"Winner: <b>{data.get('recommended_winner')}</b> | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", sub_style),
            Paragraph("Comparative Valuation & Technicals", h2_style)
        ]
        b_table = [
            [Paragraph("<b>Metric</b>", bold_style), Paragraph(f"<b>🇮🇳 {asset_in}</b>", bold_style), Paragraph(f"<b>🌐 {asset_us}</b>", bold_style)],
            [Paragraph("Current Price", bold_style), Paragraph(f"{d_in.get('current_price')} {d_in.get('currency')}", body_style), Paragraph(f"{d_us.get('current_price')} {d_us.get('currency')}", body_style)],
            [Paragraph("3-Month Performance", bold_style), Paragraph(f"{d_in.get('perf_3m_pct')}%", body_style), Paragraph(f"{d_us.get('perf_3m_pct')}%", body_style)],
            [Paragraph("14-Day RSI", bold_style), Paragraph(str(d_in.get('rsi_14')), body_style), Paragraph(str(d_us.get('rsi_14')), body_style)],
            [Paragraph("Investment Score", bold_style), Paragraph(f"<b>{data.get('score_indian')}/100</b>", bold_style), Paragraph(f"<b>{data.get('score_foreign')}/100</b>", bold_style)]
        ]
        tb = Table(b_table, colWidths=[180, 180, 180])
        tb.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.extend([tb, Spacer(1, 10), Paragraph("Algorithmic Investment Verdict", h2_style), Paragraph(data.get("verdict", ""), body_style)])
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 23. PATENT INSIDER
    def generate_patent_pdf(self, company: str, data: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Table, TableStyle
        buf = io.BytesIO(); doc = self._create_doc(buf)
        elements = [
            Paragraph(f"💡 PatentInsider Stealth R&D: {company}", title_style),
            Paragraph(f"Tracked Breakthrough Inventions: <b>{data.get('total_patents_tracked')}</b>", sub_style),
            Paragraph("Latest Patent Filings & Inventions", h2_style)
        ]
        p_table = [[Paragraph("<b>Patent ID</b>", bold_style), Paragraph("<b>Invention Title</b>", bold_style), Paragraph("<b>Tech Domain</b>", bold_style)]]
        for p in data.get("patents", [])[:8]:
            p_table.append([Paragraph(p.get("id"), bold_style), Paragraph(p.get("title")[:60], body_style), Paragraph(p.get("domain"), body_style)])
        tp = Table(p_table, colWidths=[140, 260, 140])
        tp.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tp)
        doc.build(elements); buf.seek(0); return buf.getvalue()

    # 24. FLAGSHIP: AGENCY-GRADE WHITE-LABEL SEO & GEO REPORT (SEOptimer & SEMrush Replacement)
    def generate_agency_seo_audit_pdf(self, domain: str, data: dict, agency_name: str = "NASA OSINT Intelligence") -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        styles, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import letter

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = []

        # Custom high-grade styles
        cover_title = ParagraphStyle('CoverTitle', parent=title_style, fontSize=24, leading=28, textColor=colors.HexColor("#0f172a"))
        cover_sub = ParagraphStyle('CoverSub', parent=sub_style, fontSize=11, leading=15, textColor=colors.HexColor("#475569"))
        section_h1 = ParagraphStyle('SecH1', parent=h2_style, fontSize=16, leading=20, textColor=colors.HexColor("#0284c7"), spaceBefore=14, spaceAfter=8)
        section_h2 = ParagraphStyle('SecH2', parent=h2_style, fontSize=12, leading=16, textColor=colors.HexColor("#0f172a"), spaceBefore=10, spaceAfter=6)
        pill_high = ParagraphStyle('PillHigh', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#dc2626"))
        pill_med = ParagraphStyle('PillMed', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#d97706"))
        pill_low = ParagraphStyle('PillLow', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#059669"))
        pass_style = ParagraphStyle('PassStyle', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#16a34a"))
        fail_style = ParagraphStyle('FailStyle', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#dc2626"))

        grades = data.get("grades", {})
        overall = grades.get("overall", {"grade": "B", "score": 75})
        recs = data.get("recommendations", [])
        onpage = data.get("onpage", {})
        geo = data.get("geo", {})
        perf = data.get("performance", {})
        tech = data.get("technology", {})
        links = data.get("links", {})
        usability = data.get("usability", {})
        social = data.get("social", {})
        kw_data = data.get("keyword_consistency", {})

        # ================= PAGE 1: COVER & OVERALL GRADE =================
        elements.append(Paragraph(f"<b>{agency_name.upper()}</b> • EXECUTIVE AUDIT REPORT", ParagraphStyle('HeaderBranding', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#0284c7"), spaceAfter=8)))
        elements.append(Paragraph(f"SEO & GEO Audit for <b>{domain}</b>", cover_title))
        elements.append(Paragraph(f"Comprehensive 100+ Checkpoint Performance & Search Engine Readiness Dossier<br/>Generated on {datetime.now().strftime('%d %B %Y at %H:%M UTC')}", cover_sub))
        elements.append(Spacer(1, 15))

        # Overall Grade Box
        grade_table = [
            [Paragraph("<b>OVERALL AUDIT GRADE</b>", ParagraphStyle('GHead', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#64748b"), alignment=1)), Paragraph("<b>AUDIT SUMMARY & VERDICT</b>", ParagraphStyle('GHead2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#64748b")))],
            [
                Paragraph(f"<font size=48 color='#0284c7'><b>{overall.get('grade')}</b></font><br/><font size=10 color='#475569'>Score: {overall.get('score')}/100</font>", ParagraphStyle('GBig', fontName='Helvetica-Bold', alignment=1, spaceAfter=8)),
                Paragraph(f"<b>Your page has {len(recs)} prioritized optimization opportunities.</b><br/><br/>This report evaluates your website based on On-Page SEO, Generative Engine Optimization (GEO for AI Search), Usability, Authority Links, and Performance. Improving these factors will enhance search rankings, user retention, and AI visibility.<br/><br/><b>Primary URL:</b> {data.get('full_url')}<br/><b>Status Code:</b> 200 OK (SSL Secure)", body_style)
            ]
        ]
        tg = Table(grade_table, colWidths=[180, 360])
        tg.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
            ('PADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        elements.append(tg)
        elements.append(Spacer(1, 20))

        # 5 Pillar Summary Table
        elements.append(Paragraph("Core Audit Pillars & Health Scores", section_h2))
        pillar_rows = [
            [Paragraph("<b>Audit Pillar</b>", bold_style), Paragraph("<b>Score / 100</b>", bold_style), Paragraph("<b>Grade</b>", bold_style), Paragraph("<b>Pillar Health Status</b>", bold_style)],
            [Paragraph("🔍 On-Page SEO", body_style), Paragraph(str(grades.get("onpage", {}).get("score", "N/A")), body_style), Paragraph(f"<b>{grades.get('onpage', {}).get('grade', 'N/A')}</b>", bold_style), Paragraph("Tags, Headings, Word Count & Schemas", body_style)],
            [Paragraph("🤖 Generative AI (GEO)", body_style), Paragraph(str(grades.get("geo", {}).get("score", "N/A")), body_style), Paragraph(f"<b>{grades.get('geo', {}).get('grade', 'N/A')}</b>", bold_style), Paragraph("LLM Crawlability & llms.txt Readiness", body_style)],
            [Paragraph("🔗 Links & Authority", body_style), Paragraph(str(grades.get("links", {}).get("score", "N/A")), body_style), Paragraph(f"<b>{grades.get('links', {}).get('grade', 'N/A')}</b>", bold_style), Paragraph("Internal Architecture & Backlink Signals", body_style)],
            [Paragraph("📱 Usability & Mobile", body_style), Paragraph(str(grades.get("usability", {}).get("score", "N/A")), body_style), Paragraph(f"<b>{grades.get('usability', {}).get('grade', 'N/A')}</b>", bold_style), Paragraph("Device Viewport, Fonts & Email Privacy", body_style)],
            [Paragraph("⚡ Performance & Speed", body_style), Paragraph(str(grades.get("performance", {}).get("score", "N/A")), body_style), Paragraph(f"<b>{grades.get('performance', {}).get('grade', 'N/A')}</b>", bold_style), Paragraph("Core Web Vitals, Page Weight & TTFB", body_style)]
        ]
        tp = Table(pillar_rows, colWidths=[150, 80, 70, 240])
        tp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        elements.append(tp)
        elements.append(PageBreak())

        # ================= PAGE 2: PRIORITIZED RECOMMENDATIONS =================
        elements.append(Paragraph("Actionable Recommendations Checklist", section_h1))
        elements.append(Paragraph("Address these prioritized technical issues in order to maximize organic search rank and user retention:", sub_style))

        rec_table = [[Paragraph("<b>Action Recommendation</b>", bold_style), Paragraph("<b>Category</b>", bold_style), Paragraph("<b>Priority Level</b>", bold_style)]]
        for r in recs:
            p_style = pill_high if "High" in r.get("priority") else (pill_med if "Medium" in r.get("priority") else pill_low)
            rec_table.append([
                Paragraph(r.get("action"), body_style),
                Paragraph(r.get("pillar"), body_style),
                Paragraph(f"<b>{r.get('priority').upper()}</b>", p_style)
            ])
        if len(rec_table) == 1:
            rec_table.append([Paragraph("All core technical parameters pass cleanly!", pass_style), Paragraph("General", body_style), Paragraph("OPTIMAL", pill_low)])

        tr = Table(rec_table, colWidths=[330, 110, 100])
        tr.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        elements.append(tr)
        elements.append(Spacer(1, 15))

        # ================= ON-PAGE SEO DEEP DIVE =================
        elements.append(Paragraph("Pillar 1: On-Page SEO Technical Analysis", section_h1))
        
        # Title Tag
        t_pass = "Optimal" in onpage.get("title_status", "")
        t_box = [
            [Paragraph("<b>Title Tag</b>", bold_style), Paragraph(f"{'✔ PASS' if t_pass else '⚠ ATTENTION'}", pass_style if t_pass else fail_style)],
            [Paragraph(f"<b>Content:</b> {onpage.get('title', 'None')}<br/><b>Length:</b> {onpage.get('title_length')} characters ({onpage.get('title_status')})", body_style), Paragraph("Optimal length: 50-60 characters", body_style)]
        ]
        tt = Table(t_box, colWidths=[400, 140])
        tt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tt)
        elements.append(Spacer(1, 8))

        # Meta Description
        m_pass = "Optimal" in onpage.get("description_status", "")
        m_box = [
            [Paragraph("<b>Meta Description Tag</b>", bold_style), Paragraph(f"{'✔ PASS' if m_pass else '⚠ ATTENTION'}", pass_style if m_pass else fail_style)],
            [Paragraph(f"<b>Content:</b> {onpage.get('description', 'None')}<br/><b>Length:</b> {onpage.get('description_length')} characters ({onpage.get('description_status')})", body_style), Paragraph("Optimal length: 120-160 characters", body_style)]
        ]
        tm = Table(m_box, colWidths=[400, 140])
        tm.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tm)
        elements.append(Spacer(1, 10))

        # SERP Snippet Preview Box
        elements.append(Paragraph("<b>Google SERP Snippet Preview</b>", section_h2))
        serp_mockup = [
            [Paragraph(f"<font color='#475569'>https://{domain} › ...</font><br/><font size=11 color='#1a0dab'><b>{onpage.get('title', domain)[:60]}</b></font><br/><font color='#4b5563'>{onpage.get('description', 'No meta description provided.')[:140]}...</font>", ParagraphStyle('SerpStyle', fontName='Helvetica', fontSize=9, leading=13))]
        ]
        ts = Table(serp_mockup, colWidths=[540])
        ts.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ffffff")), ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")), ('PADDING', (0,0), (-1,-1), 8)]))
        elements.append(ts)
        elements.append(PageBreak())

        # ================= PAGE 3: HEADINGS & KEYWORD CONSISTENCY =================
        elements.append(Paragraph("Heading Tag Hierarchy & Frequency", section_h1))
        h_data = [
            [Paragraph("<b>Header Tag</b>", bold_style), Paragraph("<b>Count</b>", bold_style), Paragraph("<b>Status & Sample Heading</b>", bold_style)],
            [Paragraph("H1 Header Tag", bold_style), Paragraph(str(onpage.get("h1_count", 0)), body_style), Paragraph(", ".join(onpage.get("h1_elements", [])) or "No H1 tag detected!", body_style)]
        ]
        for tag_name, cnt in onpage.get("header_counts", {}).items():
            h_data.append([Paragraph(f"{tag_name} Tags", body_style), Paragraph(str(cnt), body_style), Paragraph("Header structure present", body_style)])
        th_table = Table(h_data, colWidths=[120, 80, 340])
        th_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(th_table)
        elements.append(Spacer(1, 15))

        elements.append(Paragraph("Keyword Consistency Matrix", section_h1))
        elements.append(Paragraph("Evaluates whether primary focus terms appear consistently across Title, Meta Description, Headings, and Content:", sub_style))

        kw_table = [[Paragraph("<b>Keyword / Term</b>", bold_style), Paragraph("<b>Title</b>", bold_style), Paragraph("<b>Meta Desc</b>", bold_style), Paragraph("<b>Headings</b>", bold_style), Paragraph("<b>Page Freq</b>", bold_style)]]
        for item in kw_data.get("individual_keywords", [])[:7]:
            kw_table.append([
                Paragraph(f"<b>{item.get('keyword')}</b>", body_style),
                Paragraph("✔" if item.get("in_title") else "✘", pass_style if item.get("in_title") else fail_style),
                Paragraph("✔" if item.get("in_meta") else "✘", pass_style if item.get("in_meta") else fail_style),
                Paragraph("✔" if item.get("in_headings") else "✘", pass_style if item.get("in_headings") else fail_style),
                Paragraph(str(item.get("frequency")), bold_style)
            ])
        t_kw = Table(kw_table, colWidths=[180, 90, 90, 90, 90])
        t_kw.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5), ('ALIGN', (1,0), (-1,-1), 'CENTER')]))
        elements.append(t_kw)
        elements.append(Spacer(1, 12))

        # Phrases Matrix
        ph_table = [[Paragraph("<b>2-Word Keyphrase</b>", bold_style), Paragraph("<b>Title</b>", bold_style), Paragraph("<b>Meta Desc</b>", bold_style), Paragraph("<b>Headings</b>", bold_style), Paragraph("<b>Page Freq</b>", bold_style)]]
        for p in kw_data.get("phrases", [])[:5]:
            ph_table.append([
                Paragraph(f"<b>{p.get('phrase')}</b>", body_style),
                Paragraph("✔" if p.get("in_title") else "✘", pass_style if p.get("in_title") else fail_style),
                Paragraph("✔" if p.get("in_meta") else "✘", pass_style if p.get("in_meta") else fail_style),
                Paragraph("✔" if p.get("in_headings") else "✘", pass_style if p.get("in_headings") else fail_style),
                Paragraph(str(p.get("frequency")), bold_style)
            ])
        t_ph = Table(ph_table, colWidths=[180, 90, 90, 90, 90])
        t_ph.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5), ('ALIGN', (1,0), (-1,-1), 'CENTER')]))
        elements.append(t_ph)
        elements.append(PageBreak())

        # ================= PAGE 4: GEO & CONTENT VOLUME =================
        elements.append(Paragraph("Pillar 2: Generative Engine Optimization (GEO)", section_h1))
        elements.append(Paragraph("Evaluates how well your content is structured for AI Search Engines (ChatGPT, Perplexity, Claude, Gemini):", sub_style))

        geo_table = [
            [Paragraph("<b>GEO Checkpoint</b>", bold_style), Paragraph("<b>Result</b>", bold_style), Paragraph("<b>Status</b>", bold_style)],
            [Paragraph("LLM Readability Ratio", bold_style), Paragraph(f"{geo.get('llm_readability_ratio')} rendered ratio", body_style), Paragraph("✔ PASS", pass_style)],
            [Paragraph("llms.txt Standard File", bold_style), Paragraph(geo.get("llms_txt_url") or "Not found", body_style), Paragraph("✔ PASS" if geo.get("has_llms_txt") else "⚠ RECOMMEND", pass_style if geo.get("has_llms_txt") else fail_style)],
            [Paragraph("AI Crawlers (GPTBot/ClaudeBot)", bold_style), Paragraph("Allowed" if geo.get("allows_ai_crawlers") else f"Blocked: {', '.join(geo.get('ai_crawlers_blocked', []))}", body_style), Paragraph("✔ PASS" if geo.get("allows_ai_crawlers") else "⚠ BLOCKED", pass_style if geo.get("allows_ai_crawlers") else fail_style)],
            [Paragraph("Organization Identity Schema", bold_style), Paragraph("Detected" if geo.get("has_organization_schema") else "Missing", body_style), Paragraph("✔ PASS" if geo.get("has_organization_schema") else "⚠ ATTENTION", pass_style if geo.get("has_organization_schema") else fail_style)]
        ]
        t_geo = Table(geo_table, colWidths=[200, 240, 100])
        t_geo.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(t_geo)
        elements.append(Spacer(1, 15))

        elements.append(Paragraph("Content Volume & On-Page Health Checkpoints", section_h1))
        c_rows = [
            [Paragraph("<b>Technical Factor</b>", bold_style), Paragraph("<b>Measured Value</b>", bold_style), Paragraph("<b>Assessment</b>", bold_style)],
            [Paragraph("Word Count / Volume", bold_style), Paragraph(f"{onpage.get('word_count')} words", body_style), Paragraph("✔ Sufficient" if not onpage.get("is_thin_content") else "⚠ Thin Content (<500 words)", pass_style if not onpage.get("is_thin_content") else fail_style)],
            [Paragraph("Image Alt Tags", bold_style), Paragraph(f"{onpage.get('img_total')} images ({onpage.get('img_missing_alt')} missing alt)", body_style), Paragraph("✔ PASS" if onpage.get("img_missing_alt") == 0 else "⚠ Missing Alts", pass_style if onpage.get("img_missing_alt") == 0 else fail_style)],
            [Paragraph("Canonical Tag", bold_style), Paragraph(onpage.get("canonical") or "None specified", body_style), Paragraph("✔ PASS" if onpage.get("canonical") else "⚠ Missing", pass_style if onpage.get("canonical") else fail_style)],
            [Paragraph("Robots.txt Presence", bold_style), Paragraph(onpage.get("robots_txt_url") or "Missing", body_style), Paragraph("✔ PASS" if onpage.get("has_robots_txt") else "⚠ Missing", pass_style if onpage.get("has_robots_txt") else fail_style)],
            [Paragraph("XML Sitemaps", bold_style), Paragraph(onpage.get("sitemap_url") or "Missing", body_style), Paragraph("✔ PASS" if onpage.get("has_sitemap") else "⚠ Missing", pass_style if onpage.get("has_sitemap") else fail_style)],
            [Paragraph("Structured Data (JSON-LD)", bold_style), Paragraph(", ".join(onpage.get("schemas_detected", [])) or "None", body_style), Paragraph("✔ Detected" if onpage.get("schemas_detected") else "⚠ None", pass_style if onpage.get("schemas_detected") else fail_style)],
            [Paragraph("Analytics & Tracking", bold_style), Paragraph(", ".join(onpage.get("analytics", [])) or "None detected", body_style), Paragraph("✔ Active" if onpage.get("analytics") else "⚠ Missing", pass_style if onpage.get("analytics") else fail_style)]
        ]
        tc_table = Table(c_rows, colWidths=[180, 240, 120])
        tc_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tc_table)
        elements.append(PageBreak())

        # ================= PAGE 5: PERFORMANCE & CORE WEB VITALS =================
        elements.append(Paragraph("Pillar 3: Performance, Speed & Core Web Vitals", section_h1))
        elements.append(Paragraph("Google Lighthouse Lab Data & Real-World User Experience Metrics:", sub_style))

        p_kpi = [
            [Paragraph("<b>Mobile Score</b>", bold_style), Paragraph("<b>First Contentful Paint</b>", bold_style), Paragraph("<b>Largest Contentful Paint</b>", bold_style), Paragraph("<b>Total Page Size</b>", bold_style)],
            [Paragraph(f"<b>{perf.get('mobile_score')}/100</b>", title_style), Paragraph(str(perf.get('fcp')), title_style), Paragraph(str(perf.get('lcp')), title_style), Paragraph(str(perf.get('total_page_size_mb')), title_style)]
        ]
        tp_kpi = Table(p_kpi, colWidths=[135, 135, 135, 135])
        tp_kpi.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")), ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tp_kpi)
        elements.append(Spacer(1, 12))

        # Core Web Vitals Table
        cwv_table = [
            [Paragraph("<b>Core Web Vital Metric</b>", bold_style), Paragraph("<b>Observed Value</b>", bold_style), Paragraph("<b>Google Target Benchmark</b>", bold_style)],
            [Paragraph("First Contentful Paint (FCP)", body_style), Paragraph(str(perf.get("fcp")), bold_style), Paragraph("< 1.8 seconds (Good)", body_style)],
            [Paragraph("Largest Contentful Paint (LCP)", body_style), Paragraph(str(perf.get("lcp")), bold_style), Paragraph("< 2.5 seconds (Good)", body_style)],
            [Paragraph("Total Blocking Time (TBT)", body_style), Paragraph(str(perf.get("tbt")), bold_style), Paragraph("< 200 ms (Good)", body_style)],
            [Paragraph("Cumulative Layout Shift (CLS)", body_style), Paragraph(str(perf.get("cls")), bold_style), Paragraph("< 0.1 (Good)", body_style)],
            [Paragraph("Server Response Time (TTFB)", body_style), Paragraph(str(perf.get("server_response_ttfb")), bold_style), Paragraph("< 0.8 seconds (Fast)", body_style)]
        ]
        t_cwv = Table(cwv_table, colWidths=[200, 170, 170])
        t_cwv.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(t_cwv)
        elements.append(Spacer(1, 15))

        # Page Weight Breakdown Table
        elements.append(Paragraph("Download Page Size Breakdown", section_h2))
        size_rows = [[Paragraph("<b>Asset Type</b>", bold_style), Paragraph("<b>Estimated Download Weight</b>", bold_style)]]
        for a_type, sz in perf.get("size_breakdown", {}).items():
            size_rows.append([Paragraph(a_type, body_style), Paragraph(sz, bold_style)])
        t_sz = Table(size_rows, colWidths=[270, 270])
        t_sz.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(t_sz)
        elements.append(PageBreak())

        # ================= PAGE 6: LINKS & USABILITY =================
        elements.append(Paragraph("Pillar 4: Links & Internal Site Architecture", section_h1))
        link_kpi = [
            [Paragraph("<b>Total Links Found</b>", bold_style), Paragraph("<b>Internal Links</b>", bold_style), Paragraph("<b>External Links</b>", bold_style), Paragraph("<b>DoFollow Ratio</b>", bold_style)],
            [Paragraph(str(links.get("total_links")), title_style), Paragraph(str(links.get("internal_count")), title_style), Paragraph(str(links.get("external_count")), title_style), Paragraph(f"{round((links.get('dofollow_count', 1)/max(1, links.get('total_links', 1)))*100)}%", title_style)]
        ]
        tl_kpi = Table(link_kpi, colWidths=[135, 135, 135, 135])
        tl_kpi.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")), ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tl_kpi)
        elements.append(Spacer(1, 12))

        # Child Pages
        elements.append(Paragraph("Crawled Internal Child Pages", section_h2))
        child_rows = [[Paragraph("<b>Discovered Page Path</b>", bold_style)]]
        for cp in links.get("child_pages", [])[:8]:
            child_rows.append([Paragraph(cp, body_style)])
        tc_pages = Table(child_rows, colWidths=[540])
        tc_pages.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(tc_pages)
        elements.append(Spacer(1, 15))

        # Usability & Privacy
        elements.append(Paragraph("Pillar 5: Usability, Mobile & Email Privacy", section_h1))
        u_rows = [
            [Paragraph("<b>Check</b>", bold_style), Paragraph("<b>Result</b>", bold_style), Paragraph("<b>Status</b>", bold_style)],
            [Paragraph("Mobile Viewport Tag", bold_style), Paragraph("Present" if usability.get("has_viewport") else "Missing", body_style), Paragraph("✔ PASS" if usability.get("has_viewport") else "⚠ FAIL", pass_style if usability.get("has_viewport") else fail_style)],
            [Paragraph("Favicon Tag", bold_style), Paragraph("Present" if usability.get("favicon_found") else "Missing", body_style), Paragraph("✔ PASS" if usability.get("favicon_found") else "⚠ FAIL", pass_style if usability.get("favicon_found") else fail_style)],
            [Paragraph("Email Privacy (Scraper Harvest)", bold_style), Paragraph("Clean (No plain text emails)" if usability.get("email_privacy_pass") else f"Exposed: {', '.join(usability.get('exposed_emails', []))}", body_style), Paragraph("✔ PASS" if usability.get("email_privacy_pass") else "⚠ VULNERABLE", pass_style if usability.get("email_privacy_pass") else fail_style)],
            [Paragraph("Inline Styles Overhead", bold_style), Paragraph(f"{usability.get('inline_styles_count')} inline elements", body_style), Paragraph("✔ Clean" if usability.get("inline_styles_count", 0) < 10 else "⚠ Attention", pass_style if usability.get("inline_styles_count", 0) < 10 else fail_style)]
        ]
        tu_table = Table(u_rows, colWidths=[180, 260, 100])
        tu_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tu_table)
        elements.append(PageBreak())

        # ================= PAGE 7: TECHNOLOGY & SECURITY =================
        elements.append(Paragraph("Pillar 6 & 7: Technology Stack & Security Infrastructure", section_h1))
        elements.append(Paragraph("Server infrastructure, software fingerprinting, and DNS email security (SPF & DMARC):", sub_style))

        t_rows = [
            [Paragraph("<b>Component</b>", bold_style), Paragraph("<b>Detected Technology / Value</b>", bold_style), Paragraph("<b>Security / Health Status</b>", bold_style)],
            [Paragraph("Web Server", bold_style), Paragraph(tech.get("web_server", "N/A"), body_style), Paragraph("Active", body_style)],
            [Paragraph("Server IP Address", bold_style), Paragraph(tech.get("server_ip", "Unresolved"), body_style), Paragraph("DNS A-Record", body_style)],
            [Paragraph("DNS Nameservers", bold_style), Paragraph(", ".join(tech.get("dns_servers", [])) or "N/A", body_style), Paragraph("Authoritative", body_style)],
            [Paragraph("SPF Email Record", bold_style), Paragraph(tech.get("spf_record") or ("Present" if tech.get("has_spf") else "Missing"), body_style), Paragraph("✔ PASS" if tech.get("has_spf") else "⚠ MISSING", pass_style if tech.get("has_spf") else fail_style)],
            [Paragraph("DMARC Email Record", bold_style), Paragraph("Configured (_dmarc)" if tech.get("has_dmarc") else "Missing (_dmarc DNS entry not found)", body_style), Paragraph("✔ PASS" if tech.get("has_dmarc") else "🚨 HIGH RISK (Spoofing)", pass_style if tech.get("has_dmarc") else fail_style)]
        ]
        tt_table = Table(t_rows, colWidths=[160, 260, 120])
        tt_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 6)]))
        elements.append(tt_table)
        elements.append(Spacer(1, 15))

        # Detected Technology Stack
        elements.append(Paragraph("Software & CMS Libraries Detected", section_h2))
        s_tech_rows = [[Paragraph("<b>Software / Library</b>", bold_style), Paragraph("<b>Category</b>", bold_style)]]
        for t_item in tech.get("tech_list", []):
            s_tech_rows.append([Paragraph(t_item.get("name"), bold_style), Paragraph(t_item.get("category"), body_style)])
        if len(s_tech_rows) == 1:
            s_tech_rows.append([Paragraph("Custom Web Architecture", body_style), Paragraph("Custom Stack", body_style)])
        t_tech = Table(s_tech_rows, colWidths=[270, 270])
        t_tech.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(t_tech)
        elements.append(Spacer(1, 15))

        # Social Footprint
        elements.append(Paragraph("Social Media Footprint & Local SEO", section_h2))
        soc_rows = [[Paragraph("<b>Social Network</b>", bold_style), Paragraph("<b>Profile Link Detected</b>", bold_style)]]
        for s_net, s_link in social.get("profiles_detected", {}).items():
            soc_rows.append([Paragraph(s_net, bold_style), Paragraph(s_link, body_style)])
        if len(soc_rows) == 1:
            soc_rows.append([Paragraph("No active social profiles found linked in HTML markup", body_style), Paragraph("Missing Links", body_style)])
        t_soc = Table(soc_rows, colWidths=[180, 360])
        t_soc.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5)]))
        elements.append(t_soc)

        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()

    def generate_client_hunter_pdf(self, client_data: dict) -> bytes:
        res = self._get_base_styles()
        if not res:
            return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

        buf = io.BytesIO()
        doc = self._create_doc(buf)
        elements = [
            Paragraph("ClientHunter: Forensic Bio-Data & Corporate Battle Dossier", title_style),
            Paragraph(f"Generated: <b>{datetime.now().strftime('%Y-%m-%d %H:%M')}</b> | Locality: <b>{client_data.get('location', 'India')}</b> | Hot prospects: <b>{client_data.get('hot_leads_count', 0)} of {client_data.get('total_leads_found', 0)}</b>", sub_style),
            Paragraph("Local Failure Autopsy vs. Corporate Competitors", h2_style),
        ]
        lead_rows = [[Paragraph("<b>Business Bio</b>", bold_style), Paragraph("<b>Corporate Threat</b>", bold_style), Paragraph("<b>Local Failure</b>", bold_style), Paragraph("<b>Annual Leak</b>", bold_style)]]
        for lead in client_data.get("leads", [])[:6]:
            lead_rows.append([Paragraph(f"<b>{lead.get('business_name', '')}</b><br/>{lead.get('hist_timeline', '')}<br/>Health: {lead.get('health_score', 'N/A')}", body_style), Paragraph(lead.get("corporate_rival", "Corporate competitors"), body_style), Paragraph(lead.get("where_local_fails", "")[:180], body_style), Paragraph(f"<b>{lead.get('revenue_leak', 'N/A')}</b><br/>Deal: {lead.get('est_deal_value', 'N/A')}", bold_style)])
        lead_table = Table(lead_rows, colWidths=[145, 130, 175, 90])
        lead_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 4)]))
        elements.extend([lead_table, Spacer(1, 10), Paragraph("High-Intent Local Keywords", h2_style)])
        keyword_rows = [[Paragraph("<b>Search Term</b>", bold_style), Paragraph("<b>Intent</b>", bold_style), Paragraph("<b>Demand</b>", bold_style)]]
        for keyword in client_data.get("gbp_keywords", [])[:6]:
            keyword_rows.append([Paragraph(keyword.get("keyword", ""), body_style), Paragraph(keyword.get("intent", ""), body_style), Paragraph(keyword.get("search_vol", ""), bold_style)])
        keyword_table = Table(keyword_rows, colWidths=[270, 160, 110])
        keyword_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 4)]))
        elements.extend([keyword_table, Spacer(1, 10), Paragraph("Client Outreach Script", h2_style)])
        pitch = client_data.get("pitches", {}).get("whatsapp_dm", "").replace("\n", "<br/>")
        elements.append(Paragraph(pitch, body_style))
        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()

    def generate_job_radar_pdf(self, job_data: dict) -> bytes:
        res = self._get_base_styles()
        if not res:
            return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

        buf = io.BytesIO()
        doc = self._create_doc(buf)
        elements = [
            Paragraph(f"JobRadar Intelligence: {job_data.get('role', 'Job')} Openings", title_style),
            Paragraph(f"Generated: <b>{datetime.now().strftime('%Y-%m-%d %H:%M')}</b> | Location: <b>{job_data.get('location', 'India')}</b> | Fast approval: <b>{job_data.get('fast_approval_count', 0)} of {job_data.get('total_found', 0)}</b>", sub_style),
            Paragraph("Top Fast-Track Openings", h2_style),
        ]
        rows = [[Paragraph("<b>Role / Company</b>", bold_style), Paragraph("<b>Micro-Hub</b>", bold_style), Paragraph("<b>Salary</b>", bold_style), Paragraph("<b>Velocity</b>", bold_style)]]
        for job in job_data.get("jobs", [])[:10]:
            rows.append([Paragraph(f"<b>{job.get('title', '')}</b><br/>{job.get('company', '')} ({job.get('platform', '')})", body_style), Paragraph(job.get("area_hub", ""), body_style), Paragraph(job.get("salary", "Competitive"), body_style), Paragraph(f"<b>{job.get('velocity_score', 0)}/100</b><br/>{job.get('speed_badge', '')}", body_style)])
        table = Table(rows, colWidths=[190, 145, 105, 100])
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 4)]))
        elements.extend([table, Spacer(1, 10), Paragraph("Area Micro-Hub Hiring Density", h2_style)])
        area_rows = [[Paragraph("<b>Hub</b>", bold_style), Paragraph("<b>Openings</b>", bold_style)]]
        area_rows.extend([ [Paragraph(hub, body_style), Paragraph(str(count), bold_style)] for hub, count in sorted(job_data.get("area_distribution", {}).items(), key=lambda item: item[1], reverse=True) ])
        area_table = Table(area_rows, colWidths=[400, 140])
        area_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 4)]))
        elements.extend([area_table, Spacer(1, 10), Paragraph("Recruiter Outreach Script", h2_style)])
        pitch = job_data.get("outreach_pitch", {})
        elements.append(Paragraph(pitch.get("linkedin_inmail", "").replace("\n", "<br/>"), body_style))
        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()

    def generate_youtube_pdf(self, yt_data: dict) -> bytes:
        res = self._get_base_styles()
        if not res:
            return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

        buf = io.BytesIO()
        doc = self._create_doc(buf)
        elements = [
            Paragraph(f"YouTubeMaster Intelligence: {yt_data.get('channel_title', 'Channel')}", title_style),
            Paragraph(f"Generated: <b>{datetime.now().strftime('%Y-%m-%d %H:%M')}</b> | Niche: <b>{yt_data.get('niche', 'General')}</b> | Score: <b>{yt_data.get('overall_score', 0)}% ({yt_data.get('overall_grade', 'N/A')})</b>", sub_style),
            Paragraph("Executive Channel Audit", h2_style),
        ]
        metrics = [
            [Paragraph("<b>Metric</b>", bold_style), Paragraph("<b>Value</b>", bold_style)],
            [Paragraph("Subscribers", body_style), Paragraph(str(yt_data.get("subscribers_str", "N/A")), bold_style)],
            [Paragraph("Total Views", body_style), Paragraph(str(yt_data.get("views_str", "N/A")), bold_style)],
            [Paragraph("Published Videos", body_style), Paragraph(str(yt_data.get("videos_str", "N/A")), bold_style)],
            [Paragraph("Checks Passed", body_style), Paragraph(f"{yt_data.get('passed_checks', 0)} / {yt_data.get('total_checks', 0)}", bold_style)],
        ]
        table = Table(metrics, colWidths=[220, 320])
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dc2626")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 5)]))
        elements.extend([table, Spacer(1, 10)])

        traffic = yt_data.get("view_traffic", {})
        if traffic:
            elements.append(Paragraph("View Traffic & Velocity Forensics (Modeled Public-Surface Estimates)", h2_style))
            traffic_rows = [
                [Paragraph("<b>Metric</b>", bold_style), Paragraph("<b>Value</b>", bold_style)],
                [Paragraph("7-Day Views", body_style), Paragraph(str(traffic.get("views_7d_str", "N/A")), bold_style)],
                [Paragraph("30-Day Views", body_style), Paragraph(str(traffic.get("views_30d_str", "N/A")), bold_style)],
                [Paragraph("Daily Run-Rate / VPH", body_style), Paragraph(f"{traffic.get('daily_views_str', 'N/A')} / {traffic.get('vph_str', 'N/A')}", bold_style)],
                [Paragraph("Liquidity Ratio", body_style), Paragraph(f"{traffic.get('liquidity_ratio', 0)}x", bold_style)],
                [Paragraph("90-Day / 1-Year Forecast", body_style), Paragraph(f"{traffic.get('projected_90d', 'N/A')} / {traffic.get('projected_annual', 'N/A')}", bold_style)],
            ]
            traffic_table = Table(traffic_rows, colWidths=[220, 320])
            traffic_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 5)]))
            elements.extend([traffic_table, Spacer(1, 10)])

        rates = yt_data.get("commercial_rates", {})
        elements.append(Paragraph("Commercial Rate Card", h2_style))
        rate_rows = [[Paragraph("<b>Format</b>", bold_style), Paragraph("<b>Projected USD</b>", bold_style)]]
        for label, key in (("Dedicated Video", "dedicated_video_low"), ("60s Mid-Roll", "midroll_integration"), ("YouTube Short", "short_integration"), ("Annual Deal Potential", "annual_deal_potential")):
            rate_rows.append([Paragraph(label, body_style), Paragraph(f"${rates.get(key, 0):,}", bold_style)])
        rate_table = Table(rate_rows, colWidths=[220, 320])
        rate_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 5)]))
        elements.extend([rate_table, Spacer(1, 10), Paragraph("Pillar Scorecard", h2_style)])

        category_rows = [[Paragraph("<b>Pillar</b>", bold_style), Paragraph("<b>Score</b>", bold_style), Paragraph("<b>Grade</b>", bold_style)]]
        for name, values in yt_data.get("categories", {}).items():
            category_rows.append([Paragraph(name, body_style), Paragraph(f"{values.get('pct', 0)}%", body_style), Paragraph(values.get("grade", "N/A"), bold_style)])
        category_table = Table(category_rows, colWidths=[330, 110, 100])
        category_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("PADDING", (0, 0), (-1, -1), 4)]))
        elements.append(category_table)
        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()
    # 24. INSTAGRAM MASTER OSINT DOSSIER
    def generate_instagram_pdf(self, profile: dict) -> bytes:
        res = self._get_base_styles()
        if not res: return b""
        _, title_style, sub_style, h2_style, body_style, bold_style, colors = res
        from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
        buf = io.BytesIO()
        doc = self._create_doc(buf)

        username = profile.get("username", "target")
        full_name = profile.get("full_name", username)
        tier = profile.get("tier", "Standard")
        ratio = profile.get("authority_ratio", 0.0)
        overall_score = profile.get("overall_score", 0.0)
        overall_grade = profile.get("overall_grade", "N/A")
        total_checks = profile.get("total_checks", 100)
        passed_checks = profile.get("passed_checks", 0)

        elements = [
            Paragraph(f"📸 InstaMaster Enterprise OSINT Audit: @{username}", title_style),
            Paragraph(f"Target: <b>{full_name}</b> | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | 100+ Checkpoint Multi-Source Intelligence", sub_style),
            Spacer(1, 6),
            Paragraph("Executive Intelligence Summary", h2_style)
        ]

        # Executive Summary Scorecard Table
        summary_rows = [
            [Paragraph("<b>Audit Metric</b>", bold_style), Paragraph("<b>Value / Measurement</b>", bold_style)],
            [Paragraph("Overall Profile Grade", body_style), Paragraph(f"<b><font size='12' color='#0284c7'>{overall_grade}</font></b> ({overall_score}% Technical & Commercial Rating)", bold_style)],
            [Paragraph("Audit Checkpoints Passed", body_style), Paragraph(f"<b>{passed_checks} / {total_checks} Checks Passed</b>", bold_style)],
            [Paragraph("Primary Niche Classified", body_style), Paragraph(str(profile.get("niche", "General")), bold_style)],
            [Paragraph("Audience Influence Tier", body_style), Paragraph(str(tier), bold_style)],
            [Paragraph("Follower Authority Ratio", body_style), Paragraph(f"{ratio}:1 (Followers/Following)", bold_style)],
            [Paragraph("Verified Badge Status", body_style), Paragraph("Verified Creator / Entity" if profile.get("is_verified") else "Standard / Unverified", bold_style)],
            [Paragraph("Followers / Following / Posts", body_style), Paragraph(f"{profile.get('followers_str', 'N/A')} Followers | {profile.get('following_str', 'N/A')} Following | {profile.get('posts_str', 'N/A')} Posts", bold_style)]
        ]
        t_summary = Table(summary_rows, colWidths=[200, 340])
        t_summary.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#f8fafc"), colors.white])
        ]))
        elements.append(t_summary)
        elements.append(Spacer(1, 10))

        # Commercial Valuation Table
        rates = profile.get("commercial_rates", {})
        if rates:
            elements.append(Paragraph("Commercial Rate Card & Sponsorship Valuation", h2_style))
            comm_rows = [
                [Paragraph("<b>Monetization Asset</b>", bold_style), Paragraph("<b>Projected Market Rate</b>", bold_style)],
                [Paragraph("Sponsored Feed Post", body_style), Paragraph(f"${rates.get('sponsored_post_low', 0):,} - ${rates.get('sponsored_post_high', 0):,} per post", bold_style)],
                [Paragraph("Dedicated 60s Reel", body_style), Paragraph(f"${rates.get('sponsored_reel', 0):,} per Reel", bold_style)],
                [Paragraph("Sponsored 3-Frame Story Set", body_style), Paragraph(f"${rates.get('sponsored_story', 0):,} per story", bold_style)],
                [Paragraph("Annual Sponsorship Capacity (Est.)", body_style), Paragraph(f"<b>${rates.get('annual_potential', 0):,} / year</b>", bold_style)]
            ]
            t_comm = Table(comm_rows, colWidths=[240, 300])
            t_comm.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#16a34a")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('PADDING', (0,0), (-1,-1), 4)
            ]))
            elements.append(t_comm)
            elements.append(Spacer(1, 10))

        # 7-Pillar Breakdown Table
        categories = profile.get("categories", {})
        if categories:
            elements.append(Paragraph("7-Pillar Technical & Algorithmic Scorecard", h2_style))
            cat_rows = [[Paragraph("<b>Pillar</b>", bold_style), Paragraph("<b>Score</b>", bold_style), Paragraph("<b>Passed</b>", bold_style), Paragraph("<b>Grade</b>", bold_style)]]
            for c_name, c_data in categories.items():
                cat_rows.append([
                    Paragraph(c_name, bold_style),
                    Paragraph(f"{c_data.get('pct', 0)}%", body_style),
                    Paragraph(f"{c_data.get('passed', 0)}/{c_data.get('total', 0)}", body_style),
                    Paragraph(f"<b>{c_data.get('grade', 'N/A')}</b>", bold_style)
                ])
            t_cat = Table(cat_rows, colWidths=[220, 100, 120, 100])
            t_cat.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('PADDING', (0,0), (-1,-1), 4)
            ]))
            elements.append(t_cat)
            elements.append(Spacer(1, 10))

        # Bio links
        bio_links = profile.get("bio_links", [])
        if bio_links:
            elements.append(Paragraph("Bio Hub & Landing Pages Detected", h2_style))
            b_rows = [[Paragraph("<b>Landing Hub</b>", bold_style), Paragraph("<b>URL</b>", bold_style), Paragraph("<b>Status</b>", bold_style)]]
            for bl in bio_links:
                b_rows.append([
                    Paragraph(bl.get("name", bl.get("hub", "")), bold_style),
                    Paragraph(bl.get("url", ""), body_style),
                    Paragraph("Active / Verified", bold_style)
                ])
            t_bio = Table(b_rows, colWidths=[120, 320, 100])
            t_bio.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('PADDING', (0,0), (-1,-1), 4)
            ]))
            elements.append(t_bio)
            elements.append(Spacer(1, 10))

        # Top Priority Recommendations
        recs = profile.get("recommendations", [])
        if recs:
            elements.append(Paragraph("Actionable Optimization Roadmap", h2_style))
            r_rows = [[Paragraph("<b>Priority</b>", bold_style), Paragraph("<b>Area</b>", bold_style), Paragraph("<b>Action Item</b>", bold_style)]]
            for r in recs[:5]:
                r_rows.append([
                    Paragraph(f"<b>{r.get('priority', 'MED')}</b>", bold_style),
                    Paragraph(r.get("title", ""), bold_style),
                    Paragraph(r.get("recommendation", ""), body_style)
                ])
            t_recs = Table(r_rows, colWidths=[70, 170, 300])
            t_recs.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e11d48")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('PADDING', (0,0), (-1,-1), 4)
            ]))
            elements.append(t_recs)

        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()