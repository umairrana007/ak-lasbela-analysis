import pandas as pd
from datetime import timedelta

def get_digits(val):
    val_str = str(val).strip()
    if not any(char.isdigit() for char in val_str): return None
    digits = "".join(filter(str.isdigit, val_str))
    if len(digits) == 1: digits = "0" + digits
    return digits[-2:]

def check_cycles():
    data_path = "2023-2024-2025-2026 complete data.txt"
    df = pd.read_csv(data_path, on_bad_lines='skip', engine='python')
    df['Date_dt'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
    df = df.dropna(subset=['Date_dt']).sort_values('Date_dt')
    
    # Track hits: hits[(game, jodi, day_of_week)] = list of dates
    hits = {}
    game_list = ['GM', 'LS1', 'AK', 'LS2', 'LS3']
    
    for idx, row in df.iterrows():
        dt = row['Date_dt']
        day_of_week = dt.strftime('%A')
        for g in game_list:
            jodi = get_digits(row[g])
            if jodi:
                key = (g, jodi, day_of_week)
                if key not in hits: hits[key] = []
                hits[key].append(dt)
    
    cycle_results = []
    
    for key, dates in hits.items():
        if len(dates) < 2: continue
        
        for i in range(len(dates)-1):
            d1 = dates[i]
            d2 = dates[i+1]
            diff_days = (d2 - d1).days
            
            # 21 days = 4th week (start of it)
            # 28 days = 5th week (start of it)
            # We look for intervals around 21 or 28 days
            if diff_days in [21, 28, 35]: # 4th, 5th, or 6th week
                # Check if it was absent in between (on the same day)
                # Actually, same day occurs every 7 days.
                # So we check if it hit at 7 or 14 days.
                hit_at_7 = any((d - d1).days == 7 for d in dates)
                hit_at_14 = any((d - d1).days == 14 for d in dates)
                
                if not hit_at_7 and not hit_at_14:
                    cycle_results.append({
                        'Game': key[0],
                        'Day': key[2],
                        'Jodi': key[1],
                        'First Hit': d1.strftime('%d/%m/%Y'),
                        'Return Hit': d2.strftime('%d/%m/%Y'),
                        'Interval (Weeks)': diff_days // 7
                    })

    res_df = pd.DataFrame(cycle_results)
    if not res_df.empty:
        print(f"Total Weekly Cycle Patterns Found: {len(res_df)}")
        print("\nSample Patterns (Week 4 & 5 Repeat):")
        print(res_df.head(20).to_string(index=False))
        res_df.to_csv('weekly_cycle_results.csv', index=False)
    else:
        print("No weekly cycle patterns found.")

if __name__ == "__main__":
    check_cycles()
