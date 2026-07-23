import json
from datetime import date, datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "anshulparate2004"
OUT = Path("data/contributions.json")


def parse_count(label: str) -> int:
    head = label.split(" contribution")[0].strip()
    if head.lower() == "no":
        return 0
    return int(head.replace(",", ""))


html = requests.get(f"https://github.com/users/{USERNAME}/contributions", timeout=20).text
soup = BeautifulSoup(html, "html.parser")
days = []

for cell in soup.select("td.ContributionCalendar-day"):
    day = cell.get("data-date")
    if not day:
        continue
    count = parse_count(cell.get("aria-label", "No contributions"))
    level = int(cell.get("data-level", "0"))
    days.append({"date": day, "count": count, "level": level})

today = date.today()
year_ago = today - timedelta(days=365)
days = [d for d in days if datetime.strptime(d["date"], "%Y-%m-%d").date() >= year_ago]

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(
    json.dumps(
        {
            "username": USERNAME,
            "updated": today.isoformat(),
            "total": sum(d["count"] for d in days),
            "days": days,
        },
        indent=2,
    ),
    encoding="utf-8",
)
