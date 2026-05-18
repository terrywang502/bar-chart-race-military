"""
Military Spending Analysis Script v3
- Data starts from 1988 (first year USSR data available)
- Auto-selects all countries that ever appeared in top 7 (1988-2025)
- USSR kept as separate entity (1988-1990)
- Russia as separate entity (1992-2025)
- Comparison table:
    USSR:   1988 vs 1990 (last year with data)
    Russia: 1992 vs 2025
    Others: 1988 vs 2025

Outputs:
1. bar_chart_race_data.csv   — formatted for bar chart race visualization
2. events_table.csv          — ranking overtake events
3. growth_summary.csv        — fastest growing country per year
4. comparison_table.csv      — start vs end comparison per country
"""

import pandas as pd

# ── CONFIG ──────────────────────────────────────────────────────────────────
INPUT_FILE = 'military-spending-sipri.csv'
START_YEAR = 1988
END_YEAR   = 2025
TOP_N      = 7
# ────────────────────────────────────────────────────────────────────────────


# ── STEP 1: LOAD AND CLEAN ───────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Loading and cleaning data...")

df_raw = pd.read_csv(INPUT_FILE)
df = df_raw[
    df_raw['Code'].notna() | (df_raw['Entity'] == 'USSR')
].copy()
df = df[~df['Entity'].isin(['World'])]
df = df[(df['Year'] >= START_YEAR) & (df['Year'] <= END_YEAR)].copy()
df = df.rename(columns={
    'Entity': 'country',
    'Year':   'year',
    'Military expenditure': 'spending'
})
df['spending_billions'] = (df['spending'] / 1e9).round(2)
df = df[['country', 'year', 'spending_billions']].sort_values(['year', 'country'])

print(f"Loaded: {df['country'].nunique()} countries, {df['year'].nunique()} years")
print(f"Year range: {df['year'].min()} - {df['year'].max()}")


# ── STEP 2: AUTO-SELECT COUNTRIES THAT EVER ENTERED TOP 7 ───────────────────
print("\nSTEP 2: Finding countries that ever entered top 7...")

df['rank_all'] = df.groupby('year')['spending_billions'].rank(
    ascending=False, method='min'
).astype(int)

ever_top7 = sorted(df[df['rank_all'] <= TOP_N]['country'].unique())

print(f"Countries that ever entered top {TOP_N}:")
for c in ever_top7:
    years_in = df[(df['country'] == c) & (df['rank_all'] <= TOP_N)]['year'].tolist()
    print(f"  {c}: {years_in[0]}-{years_in[-1]}")

df = df[df['country'].isin(ever_top7)].copy()


# ── STEP 3: BAR CHART RACE DATA ──────────────────────────────────────────────
print("\nSTEP 3: Generating bar chart race data...")

bcr_df = df.pivot(index='year', columns='country', values='spending_billions')
bcr_df.index.name = 'year'
bcr_df = bcr_df.fillna(0)

bcr_df.to_csv('bar_chart_race_data.csv')
print(f"Saved: bar_chart_race_data.csv  ({bcr_df.shape[0]} years x {bcr_df.shape[1]} countries)")


# ── STEP 4: RANKING OVERTAKE EVENTS ─────────────────────────────────────────
print("\nSTEP 4: Detecting ranking overtake events...")

# Compute rank across ALL ever-top7 countries (not just current top 7)
# This ensures we detect overtakes that happen outside the top 7 threshold,
# e.g. India moving from rank 8 to rank 6, overtaking Italy and Japan.
df['rank'] = df.groupby('year')['spending_billions'].rank(
    ascending=False, method='min'
).astype(int)

years = sorted(df['year'].unique())

events = []
for i in range(1, len(years)):
    prev_year = years[i - 1]
    curr_year = years[i]

    # Use full df (all ever-top7 countries), not filtered to current top 7
    prev = df[df['year'] == prev_year].set_index('country')
    curr = df[df['year'] == curr_year].set_index('country')

    for country in curr.index:
        if country not in prev.index:
            continue
        curr_rank = curr.loc[country, 'rank']
        prev_rank = prev.loc[country, 'rank']

        if curr_rank < prev_rank:  # rank improved (lower number = higher rank)
            overtaken = [
                c for c in curr.index
                if c != country
                and c in prev.index
                and prev.loc[c, 'rank'] < prev_rank   # was ahead before
                and curr.loc[c, 'rank'] > curr_rank    # now behind
            ]
            for victim in overtaken:
                events.append({
                    'year':                 curr_year,
                    'surpasser':            country,
                    'surpassed':            victim,
                    'surpasser_rank':       int(curr_rank),
                    'surpassed_rank':       int(curr.loc[victim, 'rank']),
                    'surpasser_spending_B': curr.loc[country, 'spending_billions'],
                    'surpassed_spending_B': curr.loc[victim,  'spending_billions'],
                    'gap_B':                round(
                        curr.loc[country, 'spending_billions'] -
                        curr.loc[victim,  'spending_billions'], 2
                    )
                })

events_df = pd.DataFrame(events).drop_duplicates(
    subset=['year', 'surpasser', 'surpassed']
).sort_values('year').reset_index(drop=True)

events_df.to_csv('events_table.csv', index=False)
print(f"Found {len(events_df)} overtake events")
print("Saved: events_table.csv")


# ── STEP 5: GROWTH SUMMARY ───────────────────────────────────────────────────
print("\nSTEP 5: Calculating growth rates...")

growth_rows = []
for i in range(1, len(years)):  # years already defined from Step 4 (full df)
    prev_year = years[i - 1]
    curr_year = years[i]

    curr_data = df[df['year'] == curr_year].copy()
    prev_data = df[df['year'] == prev_year].set_index('country')['spending_billions']

    curr_data['prev'] = curr_data['country'].map(prev_data)
    curr_data['growth_B'] = curr_data['spending_billions'] - curr_data['prev']
    curr_data['growth_pct'] = (
        (curr_data['growth_B'] / curr_data['prev']) * 100
    ).round(1)

    valid = curr_data.dropna(subset=['growth_B'])
    if valid.empty:
        continue

    top_spender = curr_data.loc[curr_data['spending_billions'].idxmax()]
    fastest = valid.loc[valid['growth_B'].idxmax()]

    growth_rows.append({
        'year':               curr_year,
        'top_spender':        top_spender['country'],
        'top_spending_B':     top_spender['spending_billions'],
        'fastest_growing':    fastest['country'],
        'fastest_growth_B':   round(fastest['growth_B'], 2),
        'fastest_growth_pct': fastest['growth_pct'],
    })

growth_df = pd.DataFrame(growth_rows)
growth_df.to_csv('growth_summary.csv', index=False)
print("Saved: growth_summary.csv")


# ── STEP 6: COMPARISON TABLE ─────────────────────────────────────────────────
print("\nSTEP 6: Building comparison table...")

# Custom comparison rules:
#   USSR:   1988 vs 1990 (last year with data before dissolution)
#   Russia: 1992 vs 2025 (first year as independent state vs latest)
#   Others: 1988 vs 2025

comparison_rules = {
    'USSR':   (1988, 1990),
    'Russia': (1992, 2025),
}
default_rule = (START_YEAR, END_YEAR)

comparison_rows = []
for country in ever_top7:
    start_yr, end_yr = comparison_rules.get(country, default_rule)

    # If no data at start_yr, find earliest available year for this country
    country_data = df[df['country'] == country]
    s_start = country_data[country_data['year'] == start_yr]['spending_billions']
    if len(s_start) == 0:
        earliest_yr = int(country_data['year'].min())
        s_start = country_data[country_data['year'] == earliest_yr]['spending_billions']
        actual_start_yr = earliest_yr
        auto_fallback = True
    else:
        actual_start_yr = start_yr
        auto_fallback = False

    s_end = country_data[country_data['year'] == end_yr]['spending_billions']

    v_start = round(s_start.values[0], 2) if len(s_start) > 0 else None
    v_end   = round(s_end.values[0],   2) if len(s_end)   > 0 else None

    if v_start and v_end and v_start > 0:
        change_B   = round(v_end - v_start, 2)
        change_pct = round(((v_end - v_start) / v_start) * 100, 1)
        change_str = f"+{change_pct}%" if change_pct > 0 else f"{change_pct}%"
    else:
        change_B   = None
        change_str = 'N/A'

    # Build note
    if country == 'USSR':
        note = 'USSR: compared within dissolution period'
    elif country == 'Russia':
        note = 'Russia: from independence to 2025'
    elif auto_fallback:
        note = f'No data in {start_yr}, using earliest available year ({actual_start_yr}) vs {end_yr}'
    else:
        note = f'{START_YEAR} vs {END_YEAR}'

    comparison_rows.append({
        'country':          country,
        'start_year':       actual_start_yr,
        'start_spending_B': v_start,
        'end_year':         end_yr,
        'end_spending_B':   v_end,
        'change_B':         change_B,
        'change_pct':       change_str,
        'note':             note
    })

comparison_df = pd.DataFrame(comparison_rows)
comparison_df.to_csv('comparison_table.csv', index=False)
print("Saved: comparison_table.csv")


# ── STEP 7: PRINT KEY INSIGHTS ───────────────────────────────────────────────
print("\n" + "=" * 60)
print("KEY INSIGHTS FOR VIDEO SCRIPT")
print("=" * 60)

print(f"\n📊 ALL RANKING OVERTAKE EVENTS (top {TOP_N}, {START_YEAR}–{END_YEAR}):")
print(events_df[['year', 'surpasser', 'surpassed',
                  'surpasser_rank', 'surpasser_spending_B', 'gap_B']].to_string(index=False))

print(f"\n📈 YEARS FASTEST GROWTH WAS NOT USA:")
notable = growth_df[growth_df['fastest_growing'] != 'United States']
print(notable[['year', 'fastest_growing', 'fastest_growth_B',
               'fastest_growth_pct', 'top_spender']].to_string(index=False))

print(f"\n💡 COMPARISON TABLE (custom rules for USSR/Russia):")
print(comparison_df.to_string(index=False))

print("\n✅ Done! Files saved:")
print("  - bar_chart_race_data.csv")
print("  - events_table.csv")
print("  - growth_summary.csv")
print("  - comparison_table.csv")
