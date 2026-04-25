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

# Backtest Range: 1 Feb to 19 March 2026
start_date = pd.to_datetime('01/02/2026', format='%d/%m/%Y')
end_date = pd.to_datetime('19/03/2026', format='%d/%m/%Y')
test_df = df[(df['Date_dt'] >= start_date) & (df['Date_dt'] <= end_date)]

results = []

print(f"--- BLIND TEST REPORT ({start_date.date()} to {end_date.date()}) ---")

for g in games:
    for i, row in test_df.iterrows():
        jodi = row[f'{g}_s']
        target_set, direction = get_mapping(jodi)
        
        if target_set:
            trigger_date = row['Date_dt']
            # Look ahead 5 days for hit
            hit_row = None
            for offset in range(1, 6):
                # We search in the FULL dataframe for hits to be fair
                future_rows = df[df['Date_dt'] > trigger_date].head(offset)
                if len(future_rows) < offset: continue
                
                check_row = future_rows.iloc[-1]
                check_val = check_row[f'{g}_s']
                
                if not check_val.isdigit() or len(check_val) < 2: continue
                cv1, cv2 = int(check_val[0]), int(check_val[1])
                
                if cv1 in target_set and cv2 in target_set:
                    hit_row = check_row
                    hit_gap = offset
                    break
            
            status = "HIT" if hit_row is not None else "WAIT"
            hit_jodi = hit_row[f'{g}_s'] if hit_row is not None else "-"
            
            # Categorize hit type (Double vs Mixed)
            hit_type = "-"
            if hit_row is not None:
                hit_type = "DOUBLE" if hit_jodi[0] == hit_jodi[1] else "MIXED"

            results.append({
                'Date': row['date'], 'Game': g, 'Trigger': jodi, 
                'Target': "".join(map(str, sorted(list(target_set)))),
                'Status': status, 'Gap': hit_gap if hit_row is not None else '-',
                'Hit_Jodi': hit_jodi, 'Type': hit_type
            })

report_df = pd.DataFrame(results)

# Summary
print(f"Total Triggers: {len(report_df)}")
print(f"Total Hits: {len(report_df[report_df['Status'] == 'HIT'])}")
print(f"Hit Rate: {len(report_df[report_df['Status'] == 'HIT']) / len(report_df) * 100:.1f}%")

print("\n--- Hit Type Analysis ---")
print(report_df[report_df['Status'] == 'HIT']['Type'].value_counts())

print("\n--- Detailed Hits (Sample) ---")
print(report_df[report_df['Status'] == 'HIT'].head(15).to_string(index=False))
