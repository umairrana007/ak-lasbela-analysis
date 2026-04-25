import pandas as pd
from datetime import datetime

def get_digits(val):
    val_str = str(val).strip()
    if not any(char.isdigit() for char in val_str): return None, None
    digits = "".join(filter(str.isdigit, val_str))
    if len(digits) == 1: digits = "0" + digits
    digits = digits[-2:]
    return digits[0], digits[1]

def load_data():
    data_path = "2023-2024-2025-2026 complete data.txt"
    df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
    df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
    df = df.dropna(subset=['Date_dt']).sort_values('Date_dt')
    
    # Add most recent manual results
    results_to_add = [
        {'date': '20/04/2026', 'GM': '98', 'LS1': '50', 'AK': '88', 'LS2': '81', 'LS3': '90', 'day': 'Mon'},
        {'date': '21/04/2026', 'GM': '42', 'LS1': '25', 'AK': '84', 'LS2': '97', 'LS3': '00', 'day': 'Tue'},
        {'date': '22/04/2026', 'GM': '09', 'LS1': '52', 'AK': '41', 'LS2': '69', 'LS3': '76', 'day': 'Wed'},
        {'date': '23/04/2026', 'GM': '09', 'LS1': '84', 'AK': '51', 'LS2': '19', 'LS3': '37', 'day': 'Thu'},
        {'date': '24/04/2026', 'GM': '79', 'LS1': '79', 'AK': '05', 'LS2': '98', 'LS3': '18', 'day': 'Fri'}
    ]
    for row in results_to_add:
        row['Date_dt'] = pd.to_datetime(row['date'], format='%d/%m/%Y')
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    df = df.sort_values('Date_dt').drop_duplicates(subset=['date'])
    return df

def find_pending():
    df = load_data()
    game_list = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
    game_next = {'GM': 'LS1', 'LS1': 'AK', 'AK': 'LS2', 'LS2': 'LS3', 'LS3': 'GM'}
    
    active_pairs = []
    # Scan from 01/04/2026 to find recently triggered but pending ones
    start_analysis = pd.to_datetime('01/04/2026', format='%d/%m/%Y')
    target_date = pd.to_datetime('25/04/2026', format='%d/%m/%Y')
    
    # All pairs created since 01/04
    all_pairs = []
    
    for idx, row in df.iterrows():
        curr_date = row['Date_dt']
        if curr_date < start_analysis: continue
        
        day_results = {g: get_digits(row[g])[0] + get_digits(row[g])[1] for g in game_list if get_digits(row[g])[0] is not None}
        
        # 1. Update existing pairs
        for p in all_pairs[:]:
            if p['state'] == 0:
                for g, val in day_results.items():
                    if val == p['j1'] or val == p['j1'][::-1]:
                        p['state'] = 1
                        p['target_jodi'] = p['j2']
                        p['target_games'] = [g, game_next[g]]
                        p['first_hit_date'] = curr_date
                        break
                    elif val == p['j2'] or val == p['j2'][::-1]:
                        p['state'] = 1
                        p['target_jodi'] = p['j1']
                        p['target_games'] = [g, game_next[g]]
                        p['first_hit_date'] = curr_date
                        break
            elif p['state'] == 1:
                # Check if target hit in target games
                for tg in p['target_games']:
                    if tg in day_results:
                        val = day_results[tg]
                        if val == p['target_jodi'] or val == p['target_jodi'][::-1]:
                            p['state'] = 2 # Completed
                            break
        
        # 2. Add new pairs from today
        pairs_to_create = [('GM', 'LS1'), ('LS1', 'AK'), ('AK', 'LS2'), ('LS2', 'LS3'), ('LS3', 'GM')]
        for g1, g2 in pairs_to_create:
            o1, c1 = get_digits(row[g1])
            o2, c2 = get_digits(row[g2])
            if o1 and o2:
                all_pairs.append({
                    'j1': o1 + o2, 'j2': c1 + c2, 'origin_date': curr_date,
                    'pair_type': f"{g1}-{g2}", 'state': 0
                })

    pending = []
    for p in all_pairs:
        if p['state'] == 1:
            days_passed = (target_date - p['first_hit_date']).days
            # Only show those triggered in last 10 days
            if days_passed <= 10:
                pending.append({
                    'Target Jodi': p['target_jodi'],
                    'Games': ",".join(p['target_games']),
                    'Triggered Date': p['first_hit_date'].strftime('%d/%m/%Y'),
                    'Days Passed': days_passed,
                    'Source Pair': f"{p['j1']}-{p['j2']}"
                })
    
    pending_df = pd.DataFrame(pending)
    if not pending_df.empty:
        print(pending_df.sort_values('Days Passed', ascending=False).to_string(index=False))
    else:
        print("No pending bridge targets found.")

if __name__ == "__main__":
    find_pending()
