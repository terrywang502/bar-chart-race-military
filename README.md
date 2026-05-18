# Global Military Spending Analysis (1988–2030)

**Which countries are spending the most on their military — and who is catching up?**

A data analysis and visualization project covering global military expenditure from 1988 to 2025,
with forecasts to 2030 and a fully automated annual update pipeline.
Built with Python, Chart.js, GitHub Actions, and Claude API.

---

## Bar Chart Race Video

*Which country has the most military spending? (1988–2025)*

![Military Spending Bar Chart Race](military_spending.gif)

The video animates the rise and fall of global military powers over 37 years —
including the collapse of the USSR, China's steady climb to #2, and Russia's dramatic resurgence.

---

## Key Findings

### 1. Spending Change — Start to End Year

![Chart 1: Military spending change by country](charts/chart1_comparison.png)

> 🔗 [Interactive version](charts/chart1_comparison.html)

| Country | Start | End | Change |
|---------|-------|-----|--------|
| 🇨🇳 China | $19.9B (1989) | $335.0B (2025) | **+1,583%** |
| 🇮🇳 India | $21.1B (1988) | $93.3B (2025) | **+343%** |
| 🇷🇺 Russia | $47.5B (1992) | $158.2B (2025) | **+233%** |
| 🇸🇦 Saudi Arabia | $26.8B (1988) | $81.5B (2025) | **+204%** |
| 🇯🇵 Japan | $30.5B (1988) | $59.5B (2025) | **+95%** |
| 🇩🇪 Germany | $67.2B (1988) | $106.7B (2025) | **+59%** |
| 🇮🇹 Italy | $33.2B (1988) | $45.4B (2025) | **+37%** |
| 🇬🇧 United Kingdom | $74.4B (1988) | $88.0B (2025) | **+18%** |
| 🇫🇷 France | $56.7B (1988) | $64.5B (2025) | **+14%** |
| 🇺🇸 United States | $821.4B (1988) | $929.2B (2025) | **+13%** |
| 🇷🇺 USSR | $282.9B (1988) | $221.9B (1990) | **−22%** |

**Key insight:** The US grew just 13% in 37 years — yet still spends 2.8× more than China.
Western powers maintained dominance through existing scale, not growth.

---

### 2. Ranking Overtake Events (63 events, 1988–2025)

![Chart 2: Ranking overtake events timeline](charts/chart2_events.png)

> 🔗 [Interactive version with country filter](charts/chart2_events.html)

The interactive chart allows filtering by country to show all overtake events
involving a specific nation — as surpasser or surpassed.

**Most turbulent years:**
| Year | Events | Context |
|------|--------|---------|
| **2002** | 4 | China overtook France; Italy and Japan regained ground over Saudi Arabia |
| **2022** | 4 | Russia's Ukraine invasion spike; Saudi Arabia climbed over UK |
| **2024** | 4 | Germany and UK NATO-driven surge; both overtook India and Saudi Arabia |
| **1997** | 3 | Saudi Arabia geopolitical surge — overtook China, India, Russia simultaneously |
| **1999** | 3 | China WTO-period surge — overtook Italy, Japan, Saudi Arabia in one year |
| **2017** | 3 | Russia crashed after oil/sanctions; India, Saudi Arabia, UK all leapfrogged it |

**China's methodical climb (4 events, never reversed):**
- 1999: Overtook Italy, Japan, Saudi Arabia — rank 9 to rank 5 in one year
- 2001: Overtook Germany → #4
- 2002: Overtook France → #3
- 2005: Overtook UK → **#2**, where it has remained ever since

**India: the overlooked story (10 events as surpasser):**
- 2004: Overtook Italy and Japan simultaneously
- 2008: Overtook Germany
- 2009: Overtook France → top 5
- 2016: Overtook UK
- 2017: Overtook Russia → top 4
- 2019: Overtook Saudi Arabia → **#3**

**Russia: most volatile (appears in 20+ events — both directions)**
Swung between #3 and rank 10 multiple times across the 37-year period.

---

### 3. Fastest Growth Rate per Year (1989–2025)

![Chart 3: Fastest growth rate per year](charts/chart3_growth.png)

> 🔗 [Interactive version](charts/chart3_growth.html)

**Top single-year growth spikes:**
| Year | Country | Growth Rate | Context |
|------|---------|-------------|---------|
| 1997 | 🇸🇦 Saudi Arabia | **+35.8%** | Regional tensions + arms procurement |
| 2022 | 🇷🇺 Russia | **+29.5%** | Ukraine invasion |
| 1990 | 🇸🇦 Saudi Arabia | **+25.7%** | Gulf War period |
| 1999 | 🇨🇳 China | **+21.9%** | WTO accession period |

**Note:** The United States was the #1 spender every single year from 1988 to 2025 —
bars show fastest *growth rate*, not largest budget.

China was the fastest-growing country in **15 out of 37 years**.
Its growth rate has slowed from 20%+ in the 1990s to 6–8% in the 2020s,
but absolute dollar increases keep growing as the base expands.

---

### 4. Forecast to 2026, 2028, 2030

![Chart 4: Military spending forecast](charts/chart4_forecast.png)

> 🔗 [Interactive version with model toggle](charts/chart4_forecast.html)

Two models compared — toggle between them in the interactive chart:
- **Polynomial Regression** (degree 2) — captures long-run structural trends
- **Exponential Smoothing** (alpha=0.3) — weights recent years more heavily

| Country | 2025 Actual | 2026 Poly/Exp | 2028 Poly/Exp | 2030 Poly/Exp |
|---------|-------------|---------------|---------------|---------------|
| 🇺🇸 United States | $929B | $1,008B / $950B | $1,032B / $967B | $1,056B / $984B |
| 🇨🇳 China | $335B | $354B / $308B | $390B / $337B | $429B / $365B |
| 🇷🇺 Russia | $158B | $136B / $133B | $153B / $160B | $172B / $186B |
| 🇮🇳 India | $93B | $97B / $88B | $104B / $92B | $111B / $97B |
| 🇩🇪 Germany | $107B | $86B / $86B | $95B / $99B | $105B / $111B |
| 🇬🇧 United Kingdom | $88B | $82B / $84B | $85B / $89B | $88B / $95B |

**Three critical forecast insights:**

**Russia is projected to decline from 2025 levels** — both models predict war-level spending
($158B) is unsustainable. If conflict ends, actual may fall to $130–150B.

**China's uncertainty gap is $121B by 2030** — the largest of any country.
Polynomial captures historic acceleration; exponential smoothing reflects recent deceleration.
This divergence reflects genuine uncertainty about China's trajectory, not a model flaw.

**Germany and UK projections are likely underestimates** — models were trained on pre-2024 data.
If Germany sustains its NATO 2% GDP commitment, actual spending will significantly exceed both projections.

---

## Automated Pipeline

This project includes a fully automated annual update workflow
powered by GitHub Actions and Claude API.

### How it works

```
Triggers every May 1st (annual) or manually via GitHub Actions
            ↓
Check if SIPRI data has been updated
(MD5 hash comparison: remote vs local file)
            ↓
    No update → stop, log result
            ↓
    Update detected:
            ↓
Download new SIPRI data
            ↓
Re-run analysis scripts → regenerate all CSV outputs
            ↓
Call Claude API → generate English video script draft
            ↓
Auto-commit all updated files to GitHub
            ↓
Send email notification with link to generated script
```

### What gets automated

| Step | Tool |
|------|------|
| Data update detection | Python (MD5 hash comparison) |
| Data download | GitHub Actions + curl |
| Analysis re-run | `military_spending_analysis_v3.py` |
| Script generation | Claude API (`claude-sonnet-4-20250514`) |
| Version control | Git auto-commit |
| Notification | Gmail via GitHub Actions |

### Manual trigger

1. Go to the **Actions** tab in this repository
2. Select **"Auto Update & Generate Script"**
3. Click **"Run workflow"**

### Output

When new data is detected, the pipeline generates `generated_script.md` —
an AI-drafted English video script based on the latest data insights,
ready for human review before use.

---

## Repository Structure

```
bar-chart-race-military/
├── .github/
│   └── workflows/
│       └── auto_update.yml              # GitHub Actions pipeline
├── data/
│   └── military-spending-sipri.csv      # Raw SIPRI data via Our World in Data
├── charts/
│   ├── chart1_comparison.html           # Interactive: spending change by country
│   ├── chart1_comparison.png
│   ├── chart2_events.html               # Interactive: overtake events + country filter
│   ├── chart2_events.png
│   ├── chart3_growth.html               # Interactive: fastest growth rate per year
│   ├── chart3_growth.png
│   ├── chart4_forecast.html             # Interactive: forecast to 2030 (model toggle)
│   └── chart4_forecast.png
├── military_spending_analysis.ipynb     # Full analysis + chart generation notebook
├── military_spending_analysis_v3.py     # Data processing + CSV generation script
├── generate_script.py                   # Claude API video script generator
├── bar_chart_race_data.csv              # Formatted data for bar chart race video
├── events_table.csv                     # 63 ranking overtake events (v3: full coverage)
├── growth_summary.csv                   # Fastest growing country per year
├── comparison_table.csv                 # Start vs end year comparison per country
├── generated_script.md                  # AI-generated video script (auto-updated annually)
├── military_spending.gif                # Bar chart race demo video
└── README.md
```

---

## How to Run

**Requirements:**
```bash
pip install pandas numpy scikit-learn
```

**Step 1:** Generate CSV analysis files
```bash
python military_spending_analysis_v3.py
```

**Step 2:** Run the full notebook (generates all 4 HTML charts)
```bash
jupyter notebook military_spending_analysis.ipynb
```

**Step 3:** Generate a video script draft via Claude API
```bash
export ANTHROPIC_API_KEY=your_key_here
python generate_script.py
```

**Step 4:** Open any chart in your browser
```bash
open charts/chart1_comparison.html
```

---

## Analysis Notes

### v3 Update — Events Table Fix
Previous versions detected only overtakes between countries already ranked in the top 7
in a given year. This caused nearly half of all overtake events to be missed —
most notably India's entire rise from 2004 to 2019.

Version 3 correctly detects all overtakes among the 11 countries that ever entered the top 7,
regardless of their rank in any specific year. Total events: **33 → 63**.

### USSR vs Russia
USSR and Russia are treated as two separate entities:
- **USSR**: data available 1988–1990 only (dissolved December 1991)
- **Russia**: data begins 1992 (first year as independent state)

Russia's 1992 spending ($47.5B) was **17% of USSR's 1988 spending ($282.9B)** —
one of the most dramatic military contractions in modern history.

### Model Limitations
Forecasts are trend-based projections only. Geopolitical shocks, economic crises,
or policy changes can invalidate any model instantly.
Russia 2022 (+29.5% in a single year) demonstrates this — no model predicted it.

---

## Tools Used

| Category | Tools |
|----------|-------|
| Data Analysis | Python, Pandas, NumPy |
| Machine Learning | Scikit-learn (Polynomial Regression, Exponential Smoothing) |
| Visualization | Chart.js (interactive HTML), Matplotlib (bar chart race) |
| Automation | GitHub Actions (scheduled + manual trigger) |
| AI Integration | Claude API — automated video script generation |
| Environment | Jupyter Notebook |

---

## Data Source & Citation

**Stockholm International Peace Research Institute (SIPRI), 2026 — via Our World in Data**

> Stockholm International Peace Research Institute (2026) – with minor processing by Our World in Data.
> "Military expenditure" [dataset]. SIPRI Military Expenditure Database.

All figures are in **constant 2024 US dollars** (inflation-adjusted).
Data covers 1949–2025; this analysis uses 1988–2025.

**License:** SIPRI data is publicly available for non-commercial use with attribution.
Analysis code in this repository is released under the MIT License.
