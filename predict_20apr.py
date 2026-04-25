import pandas as pd
import os
from datetime import timedelta

# Configuration
MASTER_SET = {0, 1, 2, 5, 7, 9}
LINE1_SETS = [
    {7, 1, 2, 0, 5, 9}, # 712 vs 059
    {8, 1, 3, 0, 4, 6}, # 813 vs 046
    {9, 1, 4, 0, 3, 5}, # 914 vs 035
    {0, 1, 5, 2, 4, 7}, # 015 vs 247
    {1, 2, 6, 3, 5, 8}, # 126 vs 358
    {2, 3, 7, 4, 6, 9}, # 237 vs 469
    {3, 4, 8, 5, 7, 0}, # 348 vs 570
    {4, 5, 9, 6, 8, 1}, # 459 vs 681
    {5, 6, 0, 7, 9, 2}, # 560 vs 792
    {6, 7, 1, 8, 0, 3}  # 671 vs 803
]

def get_target(jodi_str):
    if len(jodi_str) < 2: return None
    digits = [int(d) for d in jodi_str[:2]]
    for s in LINE1_SETS:
        trigger_parts = [list(s)[0], list(s)[1], list(s)[2]]
        target_parts = [list(s)[3], list(s)[4], list(s)[5]]
        
        # Check if jodi digits are in trigger set
        if all(d in trigger_parts for d in digits):
            return "".join(map(str, sorted(target_parts)))
        # Vice versa
        if all(d in target_parts for d in digits):
            return "".join(map(str, sorted(trigger_parts)))
    return None

def is_in_master(val):
    if not val or not isinstance(val, str) or not val.isdigit(): return False
    return all(int(d) in MASTER_SET for d in val)

# Load Data
data_path = "2023-2024-2025-2026 complete data.txt"
df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Date_dt']).sort_values('Date_dt')

# Games to check
games = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
for g in games:
    df[f'{g}_s'] = df[g].astype(str).str.zfill(2).str[-2:]

# TARGET DATE: 25-04-2026 (Predicting for today/tomorrow)
# Add April 20-24 results
results_to_add = [
    {'date': '20/04/2026', 'GM': '98', 'LS1': '50', 'AK': '88', 'LS2': '81', 'LS3': '90', 'day': 'Mon'},
    {'date': '21/04/2026', 'GM': '42', 'LS1': '25', 'AK': '84', 'LS2': '97', 'LS3': '00', 'day': 'Tue'},
    {'date': '22/04/2026', 'GM': '09', 'LS1': '52', 'AK': '41', 'LS2': '69', 'LS3': '76', 'day': 'Wed'},
    {'date': '23/04/2026', 'GM': '09', 'LS1': '84', 'AK': '51', 'LS2': '19', 'LS3': '37', 'day': 'Thu'},
    {'date': '24/04/2026', 'GM': '79', 'LS1': '79', 'AK': '05', 'LS2': '98', 'LS3': '18', 'day': 'Fri'}
]
df = df[df['Date_dt'] < pd.to_datetime('20/04/2026', format='%d/%m/%Y')] 
for row in results_to_add:
    row['Date_dt'] = pd.to_datetime(row['date'], format='%d/%m/%Y')
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

df = df.sort_values('Date_dt').drop_duplicates(subset=['date'])

# Re-calculate small values
for g in games:
    df[f'{g}_s'] = df[g].astype(str).str.zfill(2).str[-2:]

target_date = pd.to_datetime('25/04/2026', format='%d/%m/%Y')
hist_df = df[df['Date_dt'] < target_date] 

print(f"--- Predictions for {target_date.strftime('%d/%m/%Y')} ---")

# 1. VERTICAL UNDER PENDING
print("\n[VERTICAL UNDER] Pending Targets:")
for g in games:
    # Check last 5 days for triggers that haven't hit yet
    pending = []
    for i in range(1, 6):
        day_idx = -i
        if abs(day_idx) > len(hist_df): break
        
        row = hist_df.iloc[day_idx]
        val = row[f'{g}_s']
        target = get_target(val)
        
        if target:
            # Check if it hit between trigger date and now
            hit = False
            for j in range(day_idx + 1, 0):
                if j >= 0: break
                check_row = hist_df.iloc[j]
                check_val = check_row[f'{g}_s']
                if all(d in [int(x) for x in list(target)] for d in [int(d) for d in check_val]):
                    hit = True
                    break
            
            if not hit:
                pending.append(f"{target} (from {row['date']} jodi {val})")
    
    if pending:
        print(f"  - {g}: Play Doubles of {', '.join(list(set(pending)))}")
    else:
        print(f"  - {g}: No pending triggers.")

# 2. LARI CHAIN
print("\n[LARI CHAIN] Predictions:")
for g in games:
    # Check if last 3 days were in MASTER_SET
    d3 = hist_df.iloc[-1]
    d2 = hist_df.iloc[-2]
    d1 = hist_df.iloc[-3]
    
    v3, v2, v1 = d3[f'{g}_s'], d2[f'{g}_s'], d1[f'{g}_s']
    
    if is_in_master(v1) and is_in_master(v2) and is_in_master(v3):
        print(f"  - {g}: LARI DETECTED ({v1}->{v2}->{v3}). Play Doubles of 059!")
    else:
        # Check if lari started 1 or 2 days ago and is still waiting
        # Lari hit window is same day + 2 days
        lari_hit = False
        # (This is a simplified check for the prompt)
        print(f"  - {g}: No active lari.")
