import pandas as pd
import os

# Line 1 Sets
LINE1_SETS = [
    {'t': {7, 1, 2}, 'tg': {0, 5, 9}},
    {'t': {8, 1, 3}, 'tg': {0, 4, 6}},
    {'t': {9, 1, 4}, 'tg': {0, 3, 5}},
    {'t': {0, 1, 5}, 'tg': {2, 4, 7}},
    {'t': {1, 2, 6}, 'tg': {3, 5, 8}},
    {'t': {2, 3, 7}, 'tg': {4, 6, 9}},
    {'t': {3, 4, 8}, 'tg': {5, 7, 0}},
    {'t': {4, 5, 9}, 'tg': {6, 8, 1}},
    {'t': {5, 6, 0}, 'tg': {7, 9, 2}},
    {'t': {6, 7, 1}, 'tg': {8, 0, 3}}
]

def get_mapping(jodi_str):
    if len(jodi_str) < 2: return None, None
    d1, d2 = int(jodi_str[0]), int(jodi_str[1])
    for s in LINE1_SETS:
        if d1 in s['t'] and d2 in s['t']: return s['tg'], 'T->TG'
        if d1 in s['tg'] and d2 in s['tg']: return s['t'], 'TG->T'
    return None, None

# Load Data
data_path = "2023-2024-2025-2026 complete data.txt"
df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Date_dt']).sort_values('Date_dt')

games = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
for g in games:
    df[f'{g}_s'] = df[g].astype(str).str.zfill(2).str[-2:]

# Vertical Hit Analysis
vertical_hits = []
for g in games:
    for i in range(len(df) - 5):
        row = df.iloc[i]
        jodi = str(row[f'{g}_s'])
        if not jodi.isdigit() or len(jodi) < 2: continue
        target_set, direction = get_mapping(jodi)
        
        if target_set:
            # Check next 5 days in same game
            for j in range(1, 6):
                if i + j >= len(df): break
                next_row = df.iloc[i+j]
                next_jodi = str(next_row[f'{g}_s'])
                if next_jodi.isdigit() and len(next_jodi) >= 2:
                    nd1, nd2 = int(next_jodi[0]), int(next_jodi[1])
                else:
                    continue
                
                if nd1 in target_set and nd2 in target_set:
                    vertical_hits.append({
                        'Game': g,
                        'Trigger_Jodi': jodi,
                        'Hit_Jodi': next_jodi,
                        'Gap': j,
                        'Trigger_Digits': sorted([int(d) for d in jodi]),
                        'Hit_Digits': sorted([nd1, nd2])
                    })
                    break # Found first hit

vh_df = pd.DataFrame(vertical_hits)

print("--- Vertical Hit Analysis (Immediate Pattern) ---")
print(f"Total Hits Analyzed: {len(vh_df)}")

# Filter for Gap 1 (Next Day)
next_day = vh_df[vh_df['Gap'] == 1]
print(f"Next Day Hits: {len(next_day)}")

# Pattern Check: Is there a common digit between Trigger and Hit?
# (In Vertical Under, trigger and target sets are disjoint, so no common digit usually)
# Wait, let's check if the SUM or something is common.

# Let's check most frequent Hit Jodis for specific Trigger Jodis
print("\nTop Trigger-Hit Pairs:")
print(vh_df.groupby(['Trigger_Jodi', 'Hit_Jodi']).size().sort_values(ascending=False).head(10))

# Let's check if specific jodis repeat
print("\nMost Frequent Hit Jodis:")
print(vh_df['Hit_Jodi'].value_counts().head(10))
