import json
from .constants import CREATOR_PERSONAS, ELITE_6_HOOKS

class AISynthesizer:
    """
    Synthesizes localized, persona-tailored OSINT data for Puter.js.
    Generates exact 6-hook video script templates grounded in real search & video data.
    """
    def __init__(self):
        pass

    def build_master_dossier_prompt(
        self,
        seo_data: dict,
        video_data: dict,
        social_data: dict,
        creator_type: str = "tech_educator",
        country: str = "US",
        pincode: str = ""
    ) -> str:
        persona_info = CREATOR_PERSONAS.get(creator_type, CREATOR_PERSONAS["tech_educator"])
        
        top_vids = video_data.get("videos", [])[:5]
        hook_shares = video_data.get("hook_dominance", {})
        pain_points = [p.get("title") for p in social_data.get("pain_points", [])[:6]]
        commercial_queries = seo_data.get("commercial", [])[:8]
        local_queries = seo_data.get("pincode_localized_queries", [])[:5]

        prompt = f"""You are an elite Cyber Threat & Viral Content Director.
Synthesize the following GROUNDED, REAL-TIME OSINT DATA into actionable content scripts.

=== TARGET AUDIENCE & GEOGRAPHY ===
• Target Niche: {seo_data.get('seed')}
• Country Code: {country}
• Locality / Pincode / Area: {pincode or 'National'}
• Creator Persona: {persona_info['name']}
• Persona Delivery Style: {persona_info['style']}

=== GROUNDED RECONNAISSANCE DATA ===
1. VERIFIED SEARCH INTENT:
- High Buyer-Intent Queries: {json.dumps(commercial_queries)}
- Hyper-Local / Pincode Searches: {json.dumps(local_queries)}

2. CURRENT LOCAL HOOK MARKET SHARE (YouTube in {country}):
{json.dumps({k: v['percentage'] for k, v in hook_shares.items()}, indent=2)}

3. TOP LOCAL BREAKOUT VIDEOS:
{json.dumps([{'title': v.get('title'), 'vph': v.get('vph'), 'detected_hook': v.get('hook')} for v in top_vids], indent=2)}

4. REAL UNFILTERED CUSTOMER PAIN POINTS (Discussions/Forums):
{json.dumps(pain_points, indent=2)}
====================================

YOUR TASK:
Generate a complete, ready-to-record **6-HOOK CONTENT BLUEPRINT** tailored strictly to this Creator Persona in {country} (Locality: {pincode or 'General'}):

For EACH of the 6 Elite Hook Archetypes below, write:
- The Spoken Hook (0-3 seconds) incorporating local context and real search terms.
- The Visual Action / On-Screen Text.
- The Retention Body (3-20 seconds) addressing the extracted pain points.
- The Call to Action (CTA).

1. 🔮 THE FORTUNE TELLER (Predicting a future change in the niche)
2. ⚡ THE CONTRARIAN (Challenging conventional wisdom / stopping mistakes)
3. 🕵️ THE INSIDER (Revealing a secret loophole or behind-the-scenes truth)
4. 🏆 THE PROVEN WINNER (Leading with verified results, numbers, or proof)
5. 🧲 THE EYE MAGNET (Visual or conceptual stunner locking attention)
6. 🧩 THE CONNECTOR (Connecting two seemingly unrelated concepts for curiosity)
"""
        return prompt

    def generate_puter_html_client(self, prompt: str, target_name: str = "Market Dossier") -> str:
        escaped_prompt = json.dumps(prompt)
        html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MZ-15 ENGINE 6-Hook Radar - {target_name}</title>
  <script src="https://js.puter.com/v2/"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0b0f19;
      color: #e2e8f0;
      margin: 0;
      padding: 24px;
    }}
    .container {{
      max-width: 980px;
      margin: 0 auto;
      background: #151d30;
      padding: 28px;
      border-radius: 12px;
      border: 1px solid #1e293b;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}
    h1 {{ color: #38bdf8; margin-top: 0; font-size: 22px; }}
    .btn {{
      background: linear-gradient(135deg, #0ea5e9, #2563eb);
      color: #fff;
      border: none;
      padding: 12px 24px;
      font-size: 15px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
    }}
    .model-select {{
      padding: 10px;
      border-radius: 6px;
      background: #1e293b;
      color: #fff;
      border: 1px solid #334155;
      margin-right: 12px;
    }}
    #output {{
      margin-top: 20px;
      background: #0a0e17;
      border: 1px solid #1e293b;
      padding: 20px;
      border-radius: 8px;
      font-size: 15px;
      line-height: 1.7;
      white-space: pre-wrap;
      color: #cbd5e1;
      min-height: 200px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🛰️ Localized 6-Hook Generator (Puter.js Free AI)</h1>
    <p style="color: #94a3b8;">Target: <strong>{target_name}</strong></p>

    <div style="margin: 16px 0;">
      <select id="modelSelect" class="model-select">
        <option value="claude-3-5-sonnet">Claude 3.5 Sonnet (Recommended)</option>
        <option value="gpt-4o">GPT-4o</option>
        <option value="mistral-large-latest">Mistral Large</option>
      </select>
      <button class="btn" id="generateBtn" onclick="runPuterAI()">Generate 6 Localized Hook Scripts</button>
    </div>

    <div id="status" style="font-size: 13px; color: #94a3b8;">Ready to stream from Puter.js...</div>
    <div id="output">Generated scripts will appear here...</div>
  </div>

  <script>
    const masterPrompt = {escaped_prompt};

    async function runPuterAI() {{
      const btn = document.getElementById('generateBtn');
      const status = document.getElementById('status');
      const output = document.getElementById('output');
      const model = document.getElementById('modelSelect').value;

      btn.disabled = true;
      btn.innerText = "Synthesizing...";
      status.innerText = `Connecting to Puter.js (${{model}})...`;

      try {{
        const response = await puter.ai.chat(masterPrompt, {{ model: model }});
        output.innerText = response;
        status.innerText = "✅ Generated 6 Localized Hook Scripts!";
      }} catch (err) {{
        output.innerText = "[-] Puter.js Error: " + err.message;
        status.innerText = "❌ Synthesis failed.";
      }} finally {{
        btn.disabled = false;
        btn.innerText = "Regenerate 6 Hook Scripts";
      }}
    }}
  </script>
</body>
</html>
"""
        return html_code
