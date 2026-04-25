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

pending_stack = [] # List of {'target': set, 'game': str, 'trigger_date': str, 'trigger_jodi': str}
log = []

for i, row in test_df.iterrows():
    day_log = {
        'Date': row['date'],
        'Results': f"GM:{row['GM_s']} LS1:{row['LS1_s']} AK:{row['AK_s']} LS2:{row['LS2_s']} LS3:{row['LS3_s']}",
        'Pending_Before': len(pending_stack),
        'Hits': [],
        'New_Triggers': []
    }
    
    # 1. Check for Hits
    remaining_pending = []
    for p in pending_stack:
        g = p['game']
        res = row[f'{g}_s']
        if res.isdigit() and len(res) >= 2:
            d1, d2 = int(res[0]), int(res[1])
            if d1 in p['target'] and d2 in p['target']:
                day_log['Hits'].append(f"{g}:{res} (Set {''.join(map(str, sorted(list(p['target']))))} Triggered {p['trigger_date']})")
                continue # Hit found, remove from pending
        
        # Limit pending to 7 days
        if (row['Date_dt'] - pd.to_datetime(p['trigger_date'], format='%d/%m/%Y')).days < 7:
            remaining_pending.append(p)
            
    pending_stack = remaining_pending
    
    # 2. Add New Triggers
    for g in games:
        target = get_target(row[f'{g}_s'])
        if target:
            new_t = {
                'target': target,
                'game': g,
                'trigger_date': row['date'],
                'trigger_jodi': row[f'{g}_s']
            }
            pending_stack.append(new_t)
            day_log['New_Triggers'].append(f"{g}:{row[f'{g}_s']}->{''.join(map(str, sorted(list(target))))}")
            
    day_log['Pending_After'] = len(pending_stack)
    log.append(day_log)

# Create a Markdown Table
with open("sim_report.md", "w") as f:
    f.write("# Simulation Report: Feb - March 2026\n\n")
    f.write("| Date | Results | New Triggers | HITS Today | Pending Count |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for entry in log:
        new_trig = ", ".join(entry['New_Triggers']) if entry['New_Triggers'] else "-"
        hits = ", ".join(entry['Hits']) if entry['Hits'] else "-"
        f.write(f"| {entry['Date']} | {entry['Results']} | {new_trig} | {hits} | {entry['Pending_After']} |\n")

print("Report generated in sim_report.md")
