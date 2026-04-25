import pandas as pd
import numpy as np

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

def get_target(d1, d2):
    for s in LINE1_SETS:
        if d1 in s['t'] and d2 in s['t']: return s['tg']
        if d1 in s['tg'] and d2 in s['tg']: return s['t']
    return None

data_path = "2023-2024-2025-2026 complete data.txt"
df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Date_dt']).sort_values('Date_dt').reset_index(drop=True)

games = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
game_data = {}
for g in games:
    vals = df[g].astype(str).str.zfill(2).str[-2:].values
    digits = []
    for v in vals:
        v_str = str(v)
        if v_str and v_str != 'nan' and v_str.isdigit() and len(v_str) >= 2:
            digits.append((int(v_str[0]), int(v_str[1])))
        else:
            digits.append(None)
    game_data[g] = digits

stats = {'Same_Game_Hit': 0, 'Cross_Game_Hit': 0, 'Total_Signals': 0}
pending = [] # (target_set, trigger_game_idx, trigger_row_idx)

for i in range(len(df)):
    # Clean up old pending (10 days)
    pending = [p for p in pending if i - p[2] < 10]
    
    # Check current row for Indicators
    for g_idx, g in enumerate(games):
        current_digits = game_data[g][i]
        if not current_digits: continue
        d1, d2 = current_digits
        
        for p_target, p_game_idx, p_row_idx in pending:
            target_set = list(p_target)
            match1 = d1 in target_set
            match2 = d2 in target_set
            
            if (match1 or match2) and not (match1 and match2):
                # INDICATOR FOUND
                indicator_digit = d1 if match1 else d2
                rem = [d for d in target_set if d != indicator_digit]
                stats['Total_Signals'] += 1
                
                # Check next 3 days
                found = False
                for offset in range(1, 4):
                    if i + offset >= len(df): break
                    
                    # Check indicator game
                    f_digits_g = game_data[g][i + offset]
                    if f_digits_g and f_digits_g[0] in rem and f_digits_g[1] in rem:
                        stats['Same_Game_Hit'] += 1
                        found = True
                        break
                    
                    # Check original game
                    f_digits_orig = game_data[games[p_game_idx]][i + offset]
                    if f_digits_orig and f_digits_orig[0] in rem and f_digits_orig[1] in rem:
                        stats['Cross_Game_Hit'] += 1
                        found = True
                        break
    
    # Add new triggers
    for g_idx, g in enumerate(games):
        digits = game_data[g][i]
        if digits:
            target = get_target(digits[0], digits[1])
            if target:
                pending.append((target, g_idx, i))

print("--- INDICATOR PATTERN ANALYSIS (OPTIMIZED) ---")
print(f"Total Indicators Found: {stats['Total_Signals']}")
print(f"Hits in Same Game (Indicator Game): {stats['Same_Game_Hit']}")
print(f"Hits in Original Game (Trigger Game): {stats['Cross_Game_Hit']}")
if stats['Total_Signals'] > 0:
    print(f"Total Success Rate: {(stats['Same_Game_Hit'] + stats['Cross_Game_Hit']) / stats['Total_Signals'] * 100:.1f}%")
