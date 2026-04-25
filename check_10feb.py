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
    if not jodi_str.isdigit() or len(jodi_str) < 2: return None, None
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

# TARGET: Predictions for 11 Feb 2026
target_date = pd.to_datetime('11/02/2026', format='%d/%m/%Y')
# History up to 10 Feb
hist_df = df[df['Date_dt'] < target_date].tail(10)

print(f"--- State of Triggers on 10/02/2026 (For 11/02 Play) ---")

for g in games:
    pending = []
    # Check last 5 days
    for i in range(1, 6):
        row = hist_df.iloc[-i]
        jodi = row[f'{g}_s']
        target_set, direction = get_mapping(jodi)
        
        if target_set:
            # Check if it hit between trigger date and 10 Feb
            hit = False
            for j in range(-i + 1, 0):
                check_row = hist_df.iloc[j]
                check_val = check_row[f'{g}_s']
                if not check_val.isdigit() or len(check_val) < 2: continue
                cv1, cv2 = int(check_val[0]), int(check_val[1])
                if cv1 in target_set and cv2 in target_set:
                    hit = True
                    break
            
            if not hit:
                pending.append(f"{''.join(map(str, sorted(list(target_set))))} (from {row['date']} jodi {jodi})")
    
    if pending:
        print(f"  - {g}: {', '.join(list(set(pending)))}")
    else:
        print(f"  - {g}: No pending triggers.")

# Result of 11 Feb
res_11 = df[df['Date_dt'] == target_date]
if not res_11.empty:
    print("\n--- Actual Result of 11/02/2026 ---")
    print(res_11[['date', 'GM', 'LS1', 'AK', 'LS2', 'LS3', 'day']].to_string(index=False))
