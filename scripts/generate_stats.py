#!/usr/bin/env python3
import json
import os
import subprocess
import urllib.request

def fetch_stats():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    query = """query {
      user(login: "Reei-dp") {
        organizations(first: 100) {
          totalCount
          nodes {
            repositories {
              totalCount
            }
          }
        }
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

    pub_commits = data["contributionsCollection"]["totalCommitContributions"]
    priv_commits = data["contributionsCollection"]["restrictedContributionsCount"]
    total_commits = pub_commits + priv_commits

    org_count = data["organizations"]["totalCount"]
    org_repos = sum(n["repositories"]["totalCount"] for n in data["organizations"]["nodes"])
    personal_repos = data["repositories"]["totalCount"]
    total_repos = personal_repos + org_repos
    prs = data["pullRequests"]["totalCount"]

    return {
        "commits": f"{total_commits:,}",
        "orgs": str(org_count),
        "total_repos": str(total_repos),
        "personal_repos": str(personal_repos),
        "org_repos": str(org_repos),
        "prs": f"{prs:,}"
    }

def generate_svg(stats, output_path):
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 175" width="100%" height="100%">
  <defs>
    <pattern id="stat-screentone" width="6" height="6" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="0.8" fill="#ffffff" fill-opacity="0.03" />
    </pattern>
  </defs>

  <style>
    .val {{ font-family: -apple-system, BlinkMacSystemFont, 'Impact', 'Arial Black', monospace; font-size: 28px; font-weight: 900; letter-spacing: 0.5px; }}
    .lbl {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 1.5px; fill: #72798f; text-transform: uppercase; }}
    .sub {{ font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: bold; letter-spacing: 0.5px; }}
    .tag {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; fill: #ff0033; font-weight: bold; letter-spacing: 1px; }}
  </style>

  <!-- Deep Dark Background -->
  <rect width="850" height="175" fill="#07080c" rx="8" stroke="#1d202e" stroke-width="1.2" />
  <rect width="850" height="175" fill="url(#stat-screentone)" rx="8" />

  <!-- Top Status Bar -->
  <text x="36" y="32" class="tag">[TELEMETRY // REEI-DP]</text>
  <text x="814" y="32" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#4d5366">ALL 21 ORGANIZATIONS &amp; PROJECTS SYNCED</text>
  <line x1="36" y1="44" x2="814" y2="44" stroke="#181a26" stroke-width="1" />

  <!-- 4 Columns Grid with Spacious Padding -->

  <!-- Column 1: Commits -->
  <g transform="translate(36, 68)">
    <text y="0" class="lbl">TOTAL COMMITS</text>
    <text y="38" class="val" fill="#f0f2f8">{stats["commits"]}</text>
    <text y="58" class="sub" fill="#ff0033">PUBLIC &amp; RESTRICTED</text>
  </g>

  <!-- Vertical Divider 1 -->
  <line x1="226" y1="64" x2="226" y2="136" stroke="#181a26" stroke-width="1" />

  <!-- Column 2: Organizations -->
  <g transform="translate(248, 68)">
    <text y="0" class="lbl">ORGANIZATIONS</text>
    <text y="38" class="val" fill="#00f5d4">{stats["orgs"]}</text>
    <text y="58" class="sub" fill="#63697e">AFFILIATED BODIES</text>
  </g>

  <!-- Vertical Divider 2 -->
  <line x1="422" y1="64" x2="422" y2="136" stroke="#181a26" stroke-width="1" />

  <!-- Column 3: Total Repositories (Personal + Orgs) -->
  <g transform="translate(444, 68)">
    <text y="0" class="lbl">TOTAL REPOS</text>
    <text y="38" class="val" fill="#ff0033">{stats["total_repos"]}</text>
    <text y="58" class="sub" fill="#63697e">{stats["personal_repos"]} USER • {stats["org_repos"]} ORGS</text>
  </g>

  <!-- Vertical Divider 3 -->
  <line x1="634" y1="64" x2="634" y2="136" stroke="#181a26" stroke-width="1" />

  <!-- Column 4: Pull Requests -->
  <g transform="translate(656, 68)">
    <text y="0" class="lbl">PULL REQUESTS</text>
    <text y="38" class="val" fill="#f0f2f8">{stats["prs"]}</text>
    <text y="58" class="sub" fill="#63697e">REVIEWS &amp; MERGES</text>
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated spacious 4-metric stats SVG at {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "stats.svg")
    stats = fetch_stats()
    generate_svg(stats, out)
