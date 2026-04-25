import pandas as pd

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
df = df.dropna(subset=['Date_dt']).sort_values('Date_dt')

games = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
for g in games:
    df[f'{g}_s'] = df[g].astype(str).str.zfill(2).str[-2:]

# Pattern Analysis
# 1. Trigger happens in Game A.
# 2. X days later, Game B shows ONE digit of the target set.
# 3. Does the PAIR of the remaining two digits show up in Game B or Game A?

stats = {'Same_Game_Hit': 0, 'Cross_Game_Hit': 0, 'Total_Signals': 0}

pending_targets = [] # List of (target_set, trigger_game, trigger_date)

for i, row in df.iterrows():
    # Update pending list (remove old ones after 10 days)
    pending_targets = [p for p in pending_targets if (row['Date_dt'] - p[2]).days < 10]
    
    # Check for hits in current row
    for g in games:
        val = str(row[f'{g}_s'])
        if val.isdigit() and len(val) >= 2:
            d1, d2 = int(val[0]), int(val[1])
        
        for p in pending_targets:
            target_set = p[0]
            if d1 in target_set and d2 in target_set:
                # This is a full hit! But we are looking for the user's specific "Indicator" logic
                pass
        
    # Check for "Indicators" (Single digit hit)
    for g in games:
        val = str(row[f'{g}_s'])
        if val.isdigit() and len(val) >= 2:
            d1, d2 = int(val[0]), int(val[1])
        
        for p in pending_targets:
            target_set = list(p[0])
            # If exactly one digit matches target set
            match1 = d1 in target_set
            match2 = d2 in target_set
            
            if (match1 or match2) and not (match1 and match2):
                indicator_digit = d1 if match1 else d2
                remaining_digits = [d for d in target_set if d != indicator_digit]
                
                # We found an indicator in Game 'g'
                # Now look for the pair of remaining_digits in the next 3 days in Game 'g' or Game 'p[1]'
                stats['Total_Signals'] += 1
                
                found_pair = False
                for offset in range(1, 4):
                    future_rows = df[df['Date_dt'] > row['Date_dt']].head(offset)
                    if len(future_rows) < offset: continue
                    f_row = future_rows.iloc[-1]
                    
                    # Check in Indicator Game (g)
                    f_val_g = str(f_row[f'{g}_s'])
                    if f_val_g.isdigit() and len(f_val_g) >= 2:
                        if int(f_val_g[0]) in remaining_digits and int(f_val_g[1]) in remaining_digits:
                            stats['Same_Game_Hit'] += 1
                            found_pair = True
                            break
                    
                    # Check in Trigger Game (p[1])
                    f_val_orig = str(f_row[f'{p[1]}_s'])
                    if f_val_orig.isdigit() and len(f_val_orig) >= 2:
                        if int(f_val_orig[0]) in remaining_digits and int(f_val_orig[1]) in remaining_digits:
                            stats['Cross_Game_Hit'] += 1
                            found_pair = True
                            break
                
    # Add new triggers from this row
    for g in games:
        target = get_mapping(row[f'{g}_s'])
        if target:
            pending_targets.append((target, g, row['Date_dt']))

print("--- INDICATOR PATTERN ANALYSIS ---")
print(f"Total Indicators Found: {stats['Total_Signals']}")
print(f"Hits in Same Game (where indicator appeared): {stats['Same_Game_Hit']}")
print(f"Hits in Original Game (where trigger appeared): {stats['Cross_Game_Hit']}")
if stats['Total_Signals'] > 0:
    print(f"Total Success Rate: {(stats['Same_Game_Hit'] + stats['Cross_Game_Hit']) / stats['Total_Signals'] * 100:.1f}%")
