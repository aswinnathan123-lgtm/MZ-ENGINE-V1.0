import re
from datetime import datetime, timezone
from urllib.parse import urlparse
import requests

class CodeIntelEngine:
    """
    Zero-key GitHub Repository & Code Intelligence Engine.
    Extracts 100% authentic OSINT from public GitHub repositories:
    - Language breakdown & exact byte distribution (Go, Rust, Python, TypeScript, etc.)
    - Live repository metrics (Stars, Forks, Open Issues, License, Topics)
    - Commit velocity radar (commits per week/month, author activity)
    """
    def __init__(self, token: str = None):
        self.headers = {
            "User-Agent": "NASA-OSINT-CodeIntel-Suite/3.4",
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

    def clean_repo_identifier(self, input_str: str) -> tuple:
        clean = input_str.strip().lower()
        if "github.com" in clean:
            parsed = urlparse(clean)
            parts = [p for p in parsed.path.split("/") if p]
            if len(parts) >= 2:
                return parts[0], parts[1]
        parts = [p.strip() for p in clean.split("/") if p.strip()]
        if len(parts) == 2:
            return parts[0], parts[1]
        return "", ""

    def _format_bytes(self, size_bytes: int) -> str:
        if size_bytes >= 1_000_000:
            return f"{size_bytes / 1_000_000:.2f} MB"
        elif size_bytes >= 1_000:
            return f"{size_bytes / 1_000:.1f} KB"
        return f"{size_bytes} Bytes"

    def analyze_repo(self, repo_input: str) -> dict:
        owner, repo = self.clean_repo_identifier(repo_input)
        if not owner or not repo:
            return {"error": "Invalid GitHub repository format. Use 'owner/repo' or full GitHub URL."}

        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        lang_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=30"

        data = {
            "owner": owner, "repo": repo, "full_name": f"{owner}/{repo}",
            "html_url": f"https://github.com/{owner}/{repo}",
            "description": "", "stars": 0, "forks": 0, "open_issues": 0, "watchers": 0,
            "license": "None", "default_branch": "main",
            "created_at": "", "updated_at": "", "pushed_at": "",
            "topics": [], "languages": [], "primary_language": "Unknown",
            "total_code_bytes": 0, "total_code_size": "0 Bytes",
            "commit_velocity": {
                "recent_sample": 0, "commits_last_7d": 0, "commits_last_30d": 0,
                "velocity_status": "NORMAL", "latest_commits": []
            }
        }

        try:
            res_repo = requests.get(repo_url, headers=self.headers, timeout=8)
            if res_repo.status_code == 404:
                return {"error": f"Repository '{owner}/{repo}' not found on GitHub."}
            elif res_repo.status_code == 403:
                return {"error": "GitHub API rate limit exceeded. Please wait a moment."}
            elif res_repo.status_code != 200:
                return {"error": f"GitHub API status code {res_repo.status_code}."}

            r_json = res_repo.json()
            data["description"] = r_json.get("description") or "No description provided."
            data["stars"] = r_json.get("stargazers_count", 0)
            data["forks"] = r_json.get("forks_count", 0)
            data["open_issues"] = r_json.get("open_issues_count", 0)
            data["watchers"] = r_json.get("subscribers_count", 0)
            data["license"] = r_json.get("license", {}).get("name") if r_json.get("license") else "No License"
            data["default_branch"] = r_json.get("default_branch", "main")
            data["created_at"] = r_json.get("created_at", "")[:10]
            data["updated_at"] = r_json.get("updated_at", "")[:10]
            data["pushed_at"] = r_json.get("pushed_at", "")[:10]
            data["topics"] = r_json.get("topics", [])
            data["primary_language"] = r_json.get("language") or "Mixed"

            # Languages
            res_lang = requests.get(lang_url, headers=self.headers, timeout=8)
            if res_lang.status_code == 200:
                l_json = res_lang.json()
                total_bytes = sum(l_json.values())
                data["total_code_bytes"] = total_bytes
                data["total_code_size"] = self._format_bytes(total_bytes)
                langs = []
                for lang_name, b_count in sorted(l_json.items(), key=lambda x: x[1], reverse=True):
                    pct = round((b_count / max(1, total_bytes)) * 100, 1)
                    langs.append({
                        "language": lang_name, "bytes": b_count,
                        "size_formatted": self._format_bytes(b_count), "percentage": pct
                    })
                data["languages"] = langs

            # Commits
            res_commits = requests.get(commits_url, headers=self.headers, timeout=8)
            if res_commits.status_code == 200:
                c_json = res_commits.json()
                if isinstance(c_json, list):
                    data["commit_velocity"]["recent_sample"] = len(c_json)
                    now_utc = datetime.now(timezone.utc)
                    c_7d = 0
                    c_30d = 0
                    recent_list = []
                    for c in c_json:
                        commit_meta = c.get("commit", {})
                        author_info = commit_meta.get("author", {})
                        commit_date_str = author_info.get("date", "")
                        author_name = author_info.get("name", "Unknown")
                        msg = commit_meta.get("message", "").splitlines()[0][:80] if commit_meta.get("message") else ""
                        sha = c.get("sha", "")[:7]
                        if commit_date_str:
                            try:
                                c_dt = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
                                diff_days = (now_utc - c_dt).total_seconds() / 86400.0
                                if diff_days <= 7: c_7d += 1
                                if diff_days <= 30: c_30d += 1
                            except: pass
                        recent_list.append({"sha": sha, "author": author_name, "date": commit_date_str[:10] if commit_date_str else "N/A", "message": msg})
                    data["commit_velocity"]["commits_last_7d"] = c_7d
                    data["commit_velocity"]["commits_last_30d"] = c_30d
                    data["commit_velocity"]["latest_commits"] = recent_list[:10]
                    if c_7d >= 15: data["commit_velocity"]["velocity_status"] = "⚡ HYPER-ACTIVE (15+ commits this week)"
                    elif c_7d >= 5: data["commit_velocity"]["velocity_status"] = "🚀 ACTIVE SPRINT (5+ commits this week)"
                    elif c_30d >= 5: data["commit_velocity"]["velocity_status"] = "🟢 REGULAR MAINTENANCE"
                    else: data["commit_velocity"]["velocity_status"] = "💤 SLOW / DORMANT"

            return data
        except Exception as e:
            return {"error": f"Failed to audit repo: {str(e)}"}
