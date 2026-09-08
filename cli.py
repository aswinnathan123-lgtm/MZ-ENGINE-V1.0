import argparse
import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.constants import WORLDWIDE_COUNTRIES, CREATOR_PERSONAS
from core.predictive_seo import PredictiveSEOEngine
from core.video_forensics import VideoForensicsEngine
from core.social_radar import SocialRadarEngine
from core.ai_synthesizer import AISynthesizer

def main():
    parser = argparse.ArgumentParser(description="NASA-Level Worldwide OSINT & 6-Hook Radar")
    parser.add_argument("--keyword", type=str, required=True, help="Topic or niche keyword")
    parser.add_argument("--country", type=str, default="US", help="Worldwide 2-letter ISO country code (e.g., US, IN, GB, CA, AU)")
    parser.add_argument("--pincode", type=str, default="", help="Hyper-local Pincode / ZIP code / Postal Area")
    parser.add_argument("--creator-type", type=str, default="tech_educator", choices=list(CREATOR_PERSONAS.keys()), help="Creator Persona")
    parser.add_argument("--output-json", type=str, default="dossier.json")

    args = parser.parse_args()

    country_name = WORLDWIDE_COUNTRIES.get(args.country.upper(), args.country.upper())
    persona_name = CREATOR_PERSONAS.get(args.creator_type, {}).get("name", args.creator_type)

    print("=" * 70)
    print("🛰️  NASA-LEVEL LOCALIZED OSINT & 6-HOOK RADAR")
    print(f"[*] Target Niche: {args.keyword}")
    print(f"[*] Country: {country_name} ({args.country.upper()})")
    if args.pincode:
        print(f"[*] Area/Pincode: {args.pincode}")
    print(f"[*] Creator Persona: {persona_name}")
    print("=" * 70)

    # 1. Localized SEO
    print("\n[1/3] 🎯 Ingesting Local Search Intent & Pincode Expansions...")
    seo_engine = PredictiveSEOEngine(country_code=args.country, pincode=args.pincode)
    seo_data = seo_engine.run_deep_matrix(args.keyword)
    print(f"    [+] Discovered {seo_data['total_queries_found']} verified local queries.")

    # 2. Localized 6-Hook Radar
    print(f"\n[2/3] 🪝 Analyzing 6-Hook Market Share in {country_name}...")
    video_engine = VideoForensicsEngine(country_code=args.country)
    video_data = video_engine.fetch_localized_youtube_radar(args.keyword, limit=20)
    
    print("    [+] Current Hook Dominance:")
    for h, stat in video_data["hook_dominance"].items():
        if stat["percentage"] > 0:
            print(f"        • {h:<24}: {stat['percentage']}% ({stat['count']} videos)")

    # 3. Social Radar
    print("\n[3/3] 🌊 Intercepting Local Customer Pain Points...")
    social_engine = SocialRadarEngine(country_code=args.country)
    pain_points = social_engine.get_community_pain_points(args.keyword)
    social_data = {"pain_points": pain_points, "audio_formulas": social_engine.get_persona_audio_formulas(args.creator_type)}
    print(f"    [+] Extracted {len(pain_points)} customer objections & problems.")

    # 4. Synthesizer
    synthesizer = AISynthesizer()
    prompt = synthesizer.build_master_dossier_prompt(
        seo_data,
        video_data,
        social_data,
        creator_type=args.creator_type,
        country=args.country,
        pincode=args.pincode
    )
    html_runner = synthesizer.generate_puter_html_client(prompt, target_name=f"{args.keyword} ({args.country})")

    with open("puter_runner.html", "w", encoding="utf-8") as f:
        f.write(html_runner)

    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump({
            "keyword": args.keyword,
            "country": args.country,
            "pincode": args.pincode,
            "creator": args.creator_type,
            "seo": seo_data,
            "video": video_data,
            "social": social_data,
            "prompt": prompt
        }, f, indent=2)

    print("\n" + "=" * 70)
    print("✅ RECONNAISSANCE COMPLETE!")
    print("Run 'python serve.py' to launch the Puter.js AI Studio without protocol errors.")
    print("=" * 70)

if __name__ == "__main__":
    main()
