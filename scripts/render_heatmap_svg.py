import json
from datetime import datetime
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

data = json.loads(DATA.read_text(encoding="utf-8"))
days = sorted(data["days"], key=lambda d: d["date"])[-371:]

cells = []
for i, day in enumerate(days):
    week = i // 7
    dow = i % 7
    x = 28 + week * 15
    y = 52 + dow * 15
    color = PALETTE[min(day["level"], 4)]
    delay = min(i * 0.008, 2.8)
    cells.append(
        f'<rect class="cell" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" '
        f'width="11" height="11" rx="2.5" fill="{color}">'
        f'<title>{day["date"]}: {day["count"]} contributions</title></rect>'
    )

svg = f'''<svg width="860" height="180" viewBox="0 0 860 180" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Contribution heatmap for {data["username"]}</title>
  <desc id="desc">{data["total"]} contributions in the last year. Last updated {data["updated"]}.</desc>
  <style>
    .bg {{ fill: #0d1117; }}
    .text {{ fill: #c9d1d9; font: 600 14px Segoe UI, Arial, sans-serif; }}
    .muted {{ fill: #8b949e; font: 500 12px Segoe UI, Arial, sans-serif; }}
    .cell {{ opacity: 0; animation: pop .65s ease forwards; }}
    @keyframes pop {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect class="bg" width="860" height="180" rx="18"/>
  <text class="text" x="28" y="30">anshul@github ~ $ ./contributions.sh</text>
  <text class="muted" x="620" y="30">{data["total"]:,} contributions / last year</text>
  <g>
    {"".join(cells)}
  </g>
  <text class="muted" x="28" y="160">Less</text>
  <rect x="62" y="151" width="10" height="10" rx="2" fill="#161b22"/>
  <rect x="78" y="151" width="10" height="10" rx="2" fill="#0e4429"/>
  <rect x="94" y="151" width="10" height="10" rx="2" fill="#006d32"/>
  <rect x="110" y="151" width="10" height="10" rx="2" fill="#26a641"/>
  <rect x="126" y="151" width="10" height="10" rx="2" fill="#39d353"/>
  <text class="muted" x="144" y="160">More</text>
</svg>
'''

OUT.write_text(svg, encoding="utf-8")
