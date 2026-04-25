import pandas as pd
from datetime import timedelta

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
    return df

def compare():
    df = load_data()
    game_list = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
    game_next = {'GM': 'LS1', 'LS1': 'AK', 'AK': 'LS2', 'LS2': 'LS3', 'LS3': 'GM'}
    
    # 1. Bridge Logic Stats
    bridge_triggers = 0
    bridge_hits_7d = 0
    
    pending_bridge = [] # [j2, target_games, hit1_date]
    
    # 2. Weekly Cycle Stats
    weekly_triggers = 0
    weekly_hits_w4 = 0
    weekly_hits_w5 = 0
    
    saturday_hits = {} # (game, jodi) -> list of dates
    
    for idx, row in df.iterrows():
        curr_date = row['Date_dt']
        is_sat = curr_date.strftime('%A') == 'Saturday'
        
        day_results = {}
        for g in game_list:
            o, c = get_digits(row[g])
            if o: day_results[g] = o + c
            
        # Check Bridge Hits
        for b in pending_bridge[:]:
            target_jodi, target_games, hit1_date = b
            if (curr_date - hit1_date).days > 7:
                pending_bridge.remove(b)
                continue
            
            if (curr_date - hit1_date).days > 0:
                hit = False
                for tg in target_games:
                    if tg in day_results:
                        val = day_results[tg]
                        if val == target_jodi or val == target_jodi[::-1]:
                            bridge_hits_7d += 1
                            pending_bridge.remove(b)
                            hit = True
                            break
                if hit: continue
        
        # Record new Bridge triggers
        pairs_to_create = [('GM', 'LS1'), ('LS1', 'AK'), ('AK', 'LS2'), ('LS2', 'LS3'), ('LS3', 'GM')]
        for g1, g2 in pairs_to_create:
            o1, c1 = get_digits(row[g1])
            o2, c2 = get_digits(row[g2])
            if o1 and o2:
                j1, j2 = o1+o2, c1+c2
                # Check if j1 or j2 just hit (simplified: every pair is a trigger if one hits)
                # But to avoid double counting, let's just say a trigger happens when one jodi appears
                # actually, my test_bridge_logic already does this. I'll just count triggers there.
                # Let's simplify: A trigger is a pair created today where one jodi hits today.
                # Wait, the jodi hitting could be J1 or J2.
                for game, val in day_results.items():
                    if val == j1 or val == j1[::-1]:
                        bridge_triggers += 1
                        pending_bridge.append([j2, [game, game_next[game]], curr_date])
                        break
                    elif val == j2 or val == j2[::-1]:
                        bridge_triggers += 1
                        pending_bridge.append([j1, [game, game_next[game]], curr_date])
                        break

        # Check Weekly Cycle Stats
        if is_sat:
            for g, val in day_results.items():
                key = (g, val)
                if key in saturday_hits:
                    # Check past saturdays
                    for prev_date in saturday_hits[key]:
                        gap = (curr_date - prev_date).days
                        if gap == 28: weekly_hits_w4 += 1
                        if gap == 35: weekly_hits_w5 += 1
                
                # Add to history
                if key not in saturday_hits: saturday_hits[key] = []
                saturday_hits[key].append(curr_date)
                weekly_triggers += 1

    print(f"--- Strategy Comparison (Total Data) ---")
    print(f"BRIDGE LOGIC (4-5 Days):")
    print(f"  Triggers: {bridge_triggers}")
    print(f"  Hits within 7 days: {bridge_hits_7d}")
    print(f"  Strike Rate: {(bridge_hits_7d/bridge_triggers)*100:.2f}%")
    
    print(f"\nWEEKLY CYCLE (4-5 Weeks):")
    print(f"  Saturday Jodis recorded: {weekly_triggers}")
    print(f"  Repeat on Week 4 (28d): {weekly_hits_w4}")
    print(f"  Repeat on Week 5 (35d): {weekly_hits_w5}")
    # Rate of repetition is naturally lower because it's a specific day
    print(f"  Total 4/5 Week Repeats: {weekly_hits_w4 + weekly_hits_w5}")
    print(f"  Strike Rate (per Jodi): {((weekly_hits_w4 + weekly_hits_w5)/weekly_triggers)*100:.2f}%")

if __name__ == "__main__":
    compare()
