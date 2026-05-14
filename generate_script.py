"""
generate_script.py
------------------
Reads the latest analysis CSVs and calls the Claude API to generate
a short-video script (English) based on the data insights.

Output:
- generated_script.md  (committed to repo)
- Console print of the script
"""

import os
import json
import urllib.request
import urllib.error
import pandas as pd
from datetime import datetime


# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY      = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL        = "claude-sonnet-4-20250514"
MAX_TOKENS   = 1000
OUTPUT_FILE  = "generated_script.md"
# ────────────────────────────────────────────────────────────────────────────


def load_analysis_data():
    """Load the three analysis CSVs and extract key insights."""

    comp   = pd.read_csv("comparison_table.csv")
    events = pd.read_csv("events_table.csv")
    growth = pd.read_csv("growth_summary.csv")

    # Top 3 changes
    comp["pct_numeric"] = (
        comp["change_pct"]
        .str.replace("%", "").str.replace("+", "")
        .astype(float)
    )
    top3 = comp.nlargest(3, "pct_numeric")[
        ["country", "start_year", "start_spending_B",
         "end_year", "end_spending_B", "change_pct"]
    ]

    # Most turbulent years
    events_per_year = (
        events.groupby("year").size()
        .sort_values(ascending=False)
        .head(3)
    )

    # Highest single-year growth spikes
    top_spikes = growth.nlargest(3, "fastest_growth_pct")[
        ["year", "fastest_growing", "fastest_growth_pct"]
    ]

    # USSR note
    ussr = comp[comp["country"] == "USSR"].iloc[0]

    summary = {
        "data_range": "1988-2025",
        "top3_growth":          top3.to_dict(orient="records"),
        "most_turbulent_years": events_per_year.to_dict(),
        "top_growth_spikes":    top_spikes.to_dict(orient="records"),
        "ussr": {
            "start_year": int(ussr["start_year"]),
            "start_B":    float(ussr["start_spending_B"]),
            "end_year":   int(ussr["end_year"]),
            "end_B":      float(ussr["end_spending_B"]),
            "change_pct": ussr["change_pct"],
        },
        "us_change_pct": (
            comp[comp["country"] == "United States"]["change_pct"].values[0]
        ),
        "total_overtake_events": len(events),
        "china_overtakes": events[events["surpasser"] == "China"][
            ["year", "surpassed", "surpasser_rank"]
        ].to_dict(orient="records"),
    }

    return summary


def build_prompt(data: dict) -> str:
    """Build the English prompt for Claude."""

    top3_text = "\n".join([
        f"- {r['country']}: {r['start_year']} ${r['start_spending_B']:.1f}B "
        f"→ {r['end_year']} ${r['end_spending_B']:.1f}B ({r['change_pct']})"
        for r in data["top3_growth"]
    ])

    spikes_text = "\n".join([
        f"- {r['year']}: {r['fastest_growing']} +{r['fastest_growth_pct']}%"
        for r in data["top_growth_spikes"]
    ])

    china_text = "\n".join([
        f"- {r['year']}: overtook {r['surpassed']}, reached #{r['surpasser_rank']}"
        for r in data["china_overtakes"]
    ])

    turbulent_text = ", ".join([
        f"{yr} ({cnt} events)"
        for yr, cnt in data["most_turbulent_years"].items()
    ])

    prompt = f"""You are a professional data storyteller who turns numbers into compelling short-video scripts.

Below are the key findings from a global military spending analysis covering {data['data_range']}:

[TOP 3 COUNTRIES BY SPENDING GROWTH]
{top3_text}

[CHINA'S RANKING CLIMB — never reversed once achieved]
{china_text}

[BIGGEST SINGLE-YEAR GROWTH SPIKES]
{spikes_text}

[MOST TURBULENT YEARS — most ranking overtakes]
{turbulent_text}

[USSR COLLAPSE]
{data['ussr']['start_year']}: USSR spent ${data['ussr']['start_B']:.1f}B
After dissolution, {data['ussr']['end_year']}: dropped to ${data['ussr']['end_B']:.1f}B ({data['ussr']['change_pct']})

[USA — #1 every single year, yet slowest grower]
Only {data['us_change_pct']} growth over 37 years — still #1 by a wide margin

[TOTAL RANKING OVERTAKE EVENTS]
{data['total_overtake_events']} events detected between 1988 and 2025

---

Using the data above, write a 48-second short-video voiceover script in English. Requirements:
1. Open with a counterintuitive hook — lead with the most shocking number to grab attention in the first 3 seconds
2. Build a clear narrative arc: hook → rise → turning point → closing
3. Language must be punchy, conversational, and easy to follow when heard (not read)
4. End with an open question or provocative statement that drives comments
5. Target length: 130-150 words (fits 48 seconds at natural voiceover pace)
6. Output the script body only — no title, no labels, no stage directions

Output the script directly:"""

    return prompt


def call_claude_api(prompt: str) -> str:
    """Call Claude API using urllib (no extra dependencies needed)."""

    if not API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

    payload = json.dumps({
        "model":      MODEL,
        "max_tokens": MAX_TOKENS,
        "messages":   [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type":      "application/json",
            "x-api-key":         API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"API error {e.code}: {error_body}")


def save_output(script: str, data: dict):
    """Save the generated script to a markdown file."""

    now         = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    top_country = data["top3_growth"][0]["country"]
    top_pct     = data["top3_growth"][0]["change_pct"]

    content = f"""# Auto-Generated Video Script

**Generated:** {now}
**Data range:** {data['data_range']}
**Trigger:** SIPRI data update detected

---

## Script

{script}

---

## Key Numbers Used

| Metric | Value |
|--------|-------|
| Highest growth country | {top_country} ({top_pct}) |
| Total ranking overtake events | {data['total_overtake_events']} |
| US 37-year growth | {data['us_change_pct']} |
| Data range | {data['data_range']} |

---

*Auto-generated by Claude API from SIPRI data. Please review before use.*
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved to {OUTPUT_FILE}")


def main():
    print("Loading analysis data...")
    data = load_analysis_data()

    print("Calling Claude API...")
    prompt = build_prompt(data)
    script = call_claude_api(prompt)

    print("\n" + "=" * 60)
    print("GENERATED SCRIPT:")
    print("=" * 60)
    print(script)
    print("=" * 60 + "\n")

    save_output(script, data)
    print("Done.")


if __name__ == "__main__":
    main()