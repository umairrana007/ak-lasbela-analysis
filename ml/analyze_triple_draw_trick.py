import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_triple_draw_trick():
    try:
        df = pd.read_csv('ml/processed_data.csv')
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    results = []

    for i in range(len(df) - 1):
        current_day = df.iloc[i]
        next_day = df.iloc[i+1]
        
        # Base Draws: GM, LS1, AK
        base_values = [current_day['gm'], current_day['ls1'], current_day['ak']]
        
        # Extract Open and Close digits
        open_digits = []
        close_digits = []
        for val in base_values:
            if pd.isna(val): continue
            v = int(val)
            open_digits.append(v // 10)
            close_digits.append(v % 10)
            
        if not open_digits or not close_digits: continue
        
        unique_opens = sorted(list(set(open_digits)))
        unique_closes = sorted(list(set(close_digits)))
        
        # Pattern Groups
        patterns = {
            'OC': [], # Day N Open + Day N Close
            'CO': [], # Day N Close + Day N Open
            'OO': [], # Day N Open + Day N Open
            'CC': [], # Day N Close + Day N Close
        }
        
        for o1 in unique_opens:
            for c1 in unique_closes:
                patterns['OC'].append(o1 * 10 + c1)
                patterns['CO'].append(c1 * 10 + o1)
        
        for o1 in unique_opens:
            for o2 in unique_opens:
                patterns['OO'].append(o1 * 10 + o2)
                
        for c1 in unique_closes:
            for c2 in unique_closes:
                patterns['CC'].append(c1 * 10 + c2)

        # Remove duplicates
        for k in patterns:
            patterns[k] = list(set(patterns[k]))
            
        day_results = {
            'date': next_day['date'],
            'hits': {k: [] for k in patterns}
        }
        
        for draw in draws:
            target_val = next_day[draw]
            if pd.isna(target_val): continue
            target_val = int(target_val)
            
            for k, p_list in patterns.items():
                if target_val in p_list:
                    day_results['hits'][k].append(draw)
                
        results.append(day_results)

    # Statistical Summary
    total_days = len(results)
    print(f"--- Refined Triple Draw Analysis (N={total_days}) ---")
    
    for k in ['OC', 'CO', 'OO', 'CC']:
        hit_days = 0
        draw_stats = {d: 0 for d in draws}
        for res in results:
            if res['hits'][k]:
                hit_days += 1
                for d in set(res['hits'][k]):
                    draw_stats[d] += 1
        
        print(f"\nPATTERN: {k}")
        print(f"Total Hit Days: {hit_days} ({(hit_days/total_days)*100:.2f}%)")
        for d, count in draw_stats.items():
            print(f"  - {d.upper()}: {(count/total_days)*100:.2f}%")

    # Haroof Analysis (Single Digits)
    print("\n--- Haroof (Single Digit) Analysis ---")
    for set_name, set_key in [('Open Set', 'opens'), ('Close Set', 'closes')]:
        hit_days = 0
        draw_stats = {d: 0 for d in draws}
        for i in range(len(df) - 1):
            curr = df.iloc[i]
            nxt = df.iloc[i+1]
            
            base = [curr['gm'], curr['ls1'], curr['ak']]
            digits = []
            for v in base:
                if pd.isna(v): continue
                digits.append(int(v) // 10 if set_key == 'opens' else int(v) % 10)
            
            u_digits = set(digits)
            day_hit = False
            for d in draws:
                val = nxt[d]
                if pd.isna(val): continue
                v = int(val)
                if (v // 10 in u_digits) or (v % 10 in u_digits):
                    draw_stats[d] += 1
                    day_hit = True
            if day_hit: hit_days += 1
            
        print(f"\nSET: {set_name}")
        print(f"Total Hit Days: {hit_days} ({(hit_days/total_days)*100:.2f}%)")
        for d, count in draw_stats.items():
            print(f"  - {d.upper()}: {(count/total_days)*100:.2f}%")

    # Find common patterns in combinations
    # (e.g., does O1+C1 hit more than O1+C2?)
    # For now, let's just confirm if the trick is viable.

if __name__ == "__main__":
    analyze_triple_draw_trick()
