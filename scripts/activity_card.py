import json
import os
import urllib.request

USERNAME = "saveliiv18"
TOKEN = os.environ["GITHUB_TOKEN"]

url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=100"

request = urllib.request.Request(
    url,
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10",
        "User-Agent": USERNAME,
    },
)

with urllib.request.urlopen(request) as response:
    events = json.load(response)

commits = 0
pull_requests = 0
issues = 0
reviews = 0

for event in events:
    event_type = event.get("type")
    payload = event.get("payload", {})

    if event_type == "PushEvent":
        commits += len(payload.get("commits", []))

    elif event_type == "PullRequestEvent":
        pull_requests += 1

    elif event_type == "IssuesEvent":
        issues += 1

    elif event_type == "PullRequestReviewEvent":
        reviews += 1

total = commits + pull_requests + issues + reviews

if total:
    commit_pct = round(commits / total * 100)
    pr_pct = round(pull_requests / total * 100)
    issue_pct = round(issues / total * 100)
    review_pct = round(reviews / total * 100)
else:
    commit_pct = pr_pct = issue_pct = review_pct = 0

# Scale graph arms according to activity percentage.
max_arm = 75

commit_arm = max(3, max_arm * commit_pct / 100)
issue_arm = max(3, max_arm * issue_pct / 100)
review_arm = max(3, max_arm * review_pct / 100)
pr_arm = max(3, max_arm * pr_pct / 100)

svg = f"""<svg width="495" height="200"
viewBox="0 0 495 200"
xmlns="http://www.w3.org/2000/svg">

<style>
.label {{
    fill: #8B949E;
    font: 14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}}
.value {{
    fill: #C9D1D9;
    font: 600 15px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}}
.axis {{
    stroke: #FFFFFF;
    stroke-width: 3;
    stroke-linecap: round;
}}
</style>

<rect x="1" y="1" width="493" height="198" rx="6"
fill="#0D1117" stroke="#30363D"/>

<!-- Commits -->
<line class="axis"
x1="247" y1="100"
x2="{247-commit_arm}" y2="100"/>

<!-- Issues -->
<line class="axis"
x1="247" y1="100"
x2="{247+issue_arm}" y2="100"/>

<!-- Code reviews -->
<line class="axis"
x1="247" y1="100"
x2="247" y2="{100-review_arm}"/>

<!-- Pull requests -->
<line class="axis"
x1="247" y1="100"
x2="247" y2="{100+pr_arm}"/>

<circle cx="247" cy="100" r="5" fill="#FFFFFF"/>

<text class="value" x="120" y="94" text-anchor="middle">{commit_pct}%</text>
<text class="label" x="120" y="113" text-anchor="middle">Commits</text>

<text class="value" x="375" y="94" text-anchor="middle">{issue_pct}%</text>
<text class="label" x="375" y="113" text-anchor="middle">Issues</text>

<text class="value" x="247" y="25" text-anchor="middle">{review_pct}%</text>
<text class="label" x="247" y="44" text-anchor="middle">Code review</text>

<text class="value" x="247" y="164" text-anchor="middle">{pr_pct}%</text>
<text class="label" x="247" y="183" text-anchor="middle">Pull requests</text>

</svg>"""

with open("activity-card.svg", "w") as f:
    f.write(svg)

print(f"Commits: {commits}")
print(f"Pull requests: {pull_requests}")
print(f"Issues: {issues}")
print(f"Code reviews: {reviews}")
