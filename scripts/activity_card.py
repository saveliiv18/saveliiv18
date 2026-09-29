import json
import os
import urllib.request

USERNAME = "saveliiv18"
TOKEN = os.environ["GITHUB_TOKEN"]

query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
    }
  }
}
"""

payload = json.dumps({
    "query": query,
    "variables": {"login": USERNAME}
}).encode("utf-8")

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": USERNAME,
    },
    method="POST",
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

if "errors" in result:
    raise RuntimeError(result["errors"])

data = result["data"]["user"]["contributionsCollection"]

commits = data["totalCommitContributions"]
pull_requests = data["totalPullRequestContributions"]
issues = data["totalIssueContributions"]
reviews = data["totalPullRequestReviewContributions"]

total = commits + pull_requests + issues + reviews

if total:
    commit_pct = round(commits / total * 100)
    pr_pct = round(pull_requests / total * 100)
    issue_pct = round(issues / total * 100)
    review_pct = round(reviews / total * 100)
else:
    commit_pct = pr_pct = issue_pct = review_pct = 0

# Length of graph arms
max_arm = 100

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

<!-- Code Reviews -->
<line class="axis"
x1="247" y1="100"
x2="247" y2="{100-review_arm}"/>

<!-- Pull Requests -->
<line class="axis"
x1="247" y1="100"
x2="247" y2="{100+pr_arm}"/>

<circle cx="247" cy="100" r="5" fill="#FFFFFF"/>

<!-- Commits -->
<text class="value" x="115" y="94"
text-anchor="middle">{commit_pct}%</text>
<text class="label" x="115" y="113"
text-anchor="middle">Commits</text>

<!-- Issues -->
<text class="value" x="380" y="94"
text-anchor="middle">{issue_pct}%</text>
<text class="label" x="380" y="113"
text-anchor="middle">Issues</text>

<!-- Reviews -->
<text class="value" x="247" y="24"
text-anchor="middle">{review_pct}%</text>
<text class="label" x="247" y="43"
text-anchor="middle">Code review</text>

<!-- PRs -->
<text class="value" x="247" y="165"
text-anchor="middle">{pr_pct}%</text>
<text class="label" x="247" y="184"
text-anchor="middle">Pull requests</text>

</svg>"""

with open("activity-card.svg", "w") as f:
    f.write(svg)

print(f"Commits: {commits} ({commit_pct}%)")
print(f"Pull requests: {pull_requests} ({pr_pct}%)")
print(f"Issues: {issues} ({issue_pct}%)")
print(f"Code reviews: {reviews} ({review_pct}%)")
