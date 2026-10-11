#!/usr/bin/env python3
import json
import os
import subprocess
import urllib.request

def fetch_stats():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    query = """query {
      user(login: "Reei-dp") {
        login
        repositories(ownerAffiliations: OWNER) {
          totalCount
        }
        pullRequests {
          totalCount
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }"""
    
    if token:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "Reei-dp-Stats-Generator"
            }
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))["data"]["user"]
    else:
        # Fallback to local gh CLI if token not directly in env
        cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
        out = subprocess.check_output(cmd).decode("utf-8")
        data = json.loads(out)["data"]["user"]

    public_commits = data["contributionsCollection"]["totalCommitContributions"]
    private_commits = data["contributionsCollection"]["restrictedContributionsCount"]
    total_commits = public_commits + private_commits
    repos = data["repositories"]["totalCount"]
    prs = data["pullRequests"]["totalCount"]

    return {
        "commits": f"{total_commits:,}",
        "repos": str(repos),
        "prs": f"{prs:,}"
    }

def generate_svg(stats, output_path):
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 190" width="100%" height="100%">
  <defs>
    <linearGradient id="stats-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0b11" />
      <stop offset="50%" stop-color="#12131d" />
      <stop offset="100%" stop-color="#08090d" />
    </linearGradient>
    <pattern id="stat-grid" width="15" height="15" patternUnits="userSpaceOnUse">
      <path d="M 15 0 L 0 0 0 15" fill="none" stroke="#ffffff" stroke-opacity="0.02" stroke-width="1" />
    </pattern>
  </defs>

  <style>
    .header-text {{ font-family: 'Courier New', monospace; font-size: 11px; font-weight: bold; fill: #ff0055; letter-spacing: 1px; }}
    .metric-value {{ font-family: 'Courier New', 'Fira Code', monospace; font-size: 26px; font-weight: 900; }}
    .metric-label {{ font-family: 'Segoe UI', -apple-system, sans-serif; font-size: 11px; fill: #7e8597; text-transform: uppercase; letter-spacing: 0.5px; }}
    .sub-note {{ font-family: 'Courier New', monospace; font-size: 10px; fill: #00f5d4; }}
  </style>

  <!-- Background -->
  <rect width="850" height="190" fill="url(#stats-bg)" rx="8" stroke="#232636" stroke-width="1.2" />
  <rect width="850" height="190" fill="url(#stat-grid)" rx="8" />

  <!-- Top bar -->
  <rect x="0" y="0" width="850" height="26" fill="#141624" rx="8" />
  <circle cx="16" cy="13" r="4" fill="#ff0055" />
  <circle cx="28" cy="13" r="4" fill="#ffbe0b" />
  <circle cx="40" cy="13" r="4" fill="#00f5d4" />
  <text x="58" y="17" class="header-text">✂ REEI-DP // METRICS OVERVIEW [THE PIT PROTOCOL]</text>
  <text x="730" y="17" font-family="'Courier New', monospace" font-size="10" fill="#00f5d4" font-weight="bold">[SYNCED]</text>

  <!-- Metric 1: Commits -->
  <g transform="translate(35, 48)">
    <rect width="230" height="110" fill="#0e1018" rx="6" stroke="#1f2233" stroke-width="1" />
    <path d="M 0 0 L 25 0 M 0 0 L 0 25" stroke="#00f5d4" stroke-width="2" />
    <text x="18" y="32" class="metric-label">Total Contributions</text>
    <text x="18" y="68" class="metric-value" fill="#00f5d4">{stats["commits"]}</text>
    <text x="18" y="92" class="sub-note">⚡ Public &amp; Private Commits</text>
  </g>

  <!-- Metric 2: Repos -->
  <g transform="translate(310, 48)">
    <rect width="230" height="110" fill="#0e1018" rx="6" stroke="#1f2233" stroke-width="1" />
    <path d="M 0 0 L 25 0 M 0 0 L 0 25" stroke="#ff0055" stroke-width="2" />
    <text x="18" y="32" class="metric-label">Repositories</text>
    <text x="18" y="68" class="metric-value" fill="#ff0055">{stats["repos"]}</text>
    <text x="18" y="92" font-family="'Courier New', monospace" font-size="10" fill="#ff708f">📦 Public &amp; Private Projects</text>
  </g>

  <!-- Metric 3: Pull Requests / Activity -->
  <g transform="translate(585, 48)">
    <rect width="230" height="110" fill="#0e1018" rx="6" stroke="#1f2233" stroke-width="1" />
    <path d="M 0 0 L 25 0 M 0 0 L 0 25" stroke="#ffbe0b" stroke-width="2" />
    <text x="18" y="32" class="metric-label">Pull Requests</text>
    <text x="18" y="68" class="metric-value" fill="#ffbe0b">{stats["prs"]}</text>
    <text x="18" y="92" font-family="'Courier New', monospace" font-size="10" fill="#ffbe0b">🔄 Contributions &amp; Merges</text>
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated stats SVG at {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "stats.svg")
    stats = fetch_stats()
    generate_svg(stats, out)
