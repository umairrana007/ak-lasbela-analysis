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

def get_target(jodi_str):
    jodi_str = str(jodi_str)
    if not jodi_str.isdigit() or len(jodi_str) < 2: return None
    d1, d2 = int(jodi_str[0]), int(jodi_str[1])
    for s in LINE1_SETS:
        if d1 in s['t'] and d2 in s['t']: return s['tg']
        if d1 in s['tg'] and d2 in s['tg']: return s['t']
    return None

# Load Data
data_path = "2023-2024-2025-2026 complete data.txt"
df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Date_dt']).sort_values('Date_dt').reset_index(drop=True)

games = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
for g in games:
    df[f'{g}_s'] = df[g].astype(str).str.zfill(2).str[-2:]

# Backtest for Feb and March 2026
start_date = pd.to_datetime('01/02/2026', format='%d/%m/%Y')
end_date = pd.to_datetime('31/03/2026', format='%d/%m/%Y')
test_df = df[(df['Date_dt'] >= start_date) & (df['Date_dt'] <= end_date)]

trigger_ledger = [] # Each trigger is a dict

for i, row in test_df.iterrows():
    current_date = row['Date_dt']
    
    # 1. Check existing triggers for hits
    for trig in trigger_ledger:
        if trig['Status'] == 'PENDING':
            g = trig['Game']
            res = row[f'{g}_s']
            if res.isdigit() and len(res) >= 2:
                d1, d2 = int(res[0]), int(res[1])
                if d1 in trig['TargetSet'] and d2 in trig['TargetSet']:
                    trig['Status'] = 'HIT'
                    trig['HitDate'] = row['date']
                    trig['Gap'] = (current_date - pd.to_datetime(trig['CreatedDate'], format='%d/%m/%Y')).days
    
    # 2. Capture new triggers from today
    for g in games:
        target = get_target(row[f'{g}_s'])
        if target:
            trigger_ledger.append({
                'CreatedDate': row['date'],
                'Game': g,
                'SourceJodi': row[f'{g}_s'],
                'TargetSet': target,
                'HitDate': '-',
                'Status': 'PENDING',
                'Gap': '-'
            })

# Create a Markdown Table
with open("trigger_ledger.md", "w") as f:
    f.write("# Trigger Ledger: Feb - March 2026\n\n")
    f.write("| Created Date | Source Record | Game | Source Jodi | Target Set | Hit Date | Hit Record | Status | Gap |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
    
    # Pre-calculate full records for faster lookup
    df['FullRecord'] = df.apply(lambda r: f"{r['GM_s']}.{r['LS1_s']}.{r['AK_s']}.{r['LS2_s']}.{r['LS3_s']}", axis=1)
    record_map = dict(zip(df['date'], df['FullRecord']))

    for t in trigger_ledger:
        t_set_str = "".join(map(str, sorted(list(t['TargetSet']))))
        src_record = record_map.get(t['CreatedDate'], "-")
        hit_record = record_map.get(t['HitDate'], "-")
        f.write(f"| {t['CreatedDate']} | {src_record} | {t['Game']} | {t['SourceJodi']} | {t_set_str} | {t['HitDate']} | {hit_record} | {t['Status']} | {t['Gap']} |\n")

print("Ledger generated in trigger_ledger.md")
