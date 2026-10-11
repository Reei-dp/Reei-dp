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
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 140" width="100%" height="100%">
  <defs>
    <pattern id="stat-tone" width="6" height="6" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="0.8" fill="#ffffff" fill-opacity="0.04" />
    </pattern>
  </defs>

  <style>
    .val {{ font-family: -apple-system, BlinkMacSystemFont, 'Impact', 'Arial Black', monospace; font-size: 32px; font-weight: 900; }}
    .lbl {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 1.5px; fill: #63687a; text-transform: uppercase; }}
    .tag {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; fill: #ff0033; font-weight: bold; }}
  </style>

  <!-- Dark Background -->
  <rect width="850" height="140" fill="#070709" />
  <rect width="850" height="140" fill="url(#stat-tone)" />

  <!-- Borders -->
  <rect x="18" y="14" width="814" height="112" fill="none" stroke="#1f2029" stroke-width="1.2" />
  <rect x="22" y="18" width="806" height="104" fill="none" stroke="#ff0033" stroke-width="0.75" stroke-opacity="0.3" />

  <!-- Top Status -->
  <text x="36" y="34" class="tag">[TELEMETRY // REEI-DP]</text>
  <text x="814" y="34" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="10" fill="#4d5263">ALL REPOSITORIES SYNCED</text>

  <!-- Metric 1: Commits -->
  <g transform="translate(36, 48)">
    <text y="20" class="lbl">Total Contributions</text>
    <text y="58" class="val" fill="#f0f1f5">{stats["commits"]}</text>
    <text y="72" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#ff0033">PUBLIC &amp; RESTRICTED</text>
  </g>

  <!-- Divider 1 -->
  <line x1="290" y1="52" x2="290" y2="108" stroke="#1a1c24" stroke-width="1" />

  <!-- Metric 2: Repositories -->
  <g transform="translate(320, 48)">
    <text y="20" class="lbl">Repositories</text>
    <text y="58" class="val" fill="#ff0033">{stats["repos"]}</text>
    <text y="72" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#63687a">ACTIVE PROJECTS</text>
  </g>

  <!-- Divider 2 -->
  <line x1="560" y1="52" x2="560" y2="108" stroke="#1a1c24" stroke-width="1" />

  <!-- Metric 3: Pull Requests -->
  <g transform="translate(590, 48)">
    <text y="20" class="lbl">Pull Requests</text>
    <text y="58" class="val" fill="#f0f1f5">{stats["prs"]}</text>
    <text y="72" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#63687a">CODE REVIEWS &amp; MERGES</text>
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "stats.svg")
    stats = fetch_stats()
    generate_svg(stats, out)
