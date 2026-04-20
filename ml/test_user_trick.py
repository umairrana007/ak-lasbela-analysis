import pandas as pd
import json
from datetime import datetime, timedelta

def test_user_trick():
    # Load data
    try:
        df = pd.read_csv('ml/processed_data.csv')
        df['date'] = pd.to_datetime(df['date'])
    except:
        print("Data file not found.")
        return

    print("--- Backtesting User's Cross-Match & Cycle Trick ---")
    
    # Example starting from 01/02/2026 as per user
    start_date = datetime(2026, 2, 1)
    
    # Filter data from Feb 2026 onwards for the trace
    test_df = df[df['date'] >= start_date].copy()
    
    if test_df.empty:
        print("No data found for the specified period.")
        return

    # Let's trace the specific example provided
    # 01/02/2026: LS1=41, AK=25
    day1 = test_df[test_df['date'] == '2026-02-01']
    if not day1.empty:
        ls1 = str(int(day1.iloc[0]['ls1'])).zfill(2)
        ak = str(int(day1.iloc[0]['ak'])).zfill(2)
        digits = set(ls1) | set(ak)
        jodis = []
        for d1 in digits:
            for d2 in digits:
                jodis.append(int(d1 + d2))
        
        print(f"Base Date: 01/02/2026 | LS1: {ls1}, AK: {ak}")
        print(f"Generated Jodis: {sorted(list(set(jodis)))}")
        
        # Look for first appearance in AK or LS2
        appearance = test_df[(test_df['date'] > '2026-02-01') & 
                             (test_df['ak'].isin(jodis) | test_df['ls2'].isin(jodis))].head(1)
        
        if not appearance.empty:
            app_date = appearance.iloc[0]['date']
            app_val = appearance.iloc[0]['ak'] if appearance.iloc[0]['ak'] in jodis else appearance.iloc[0]['ls2']
            print(f"First Appearance: {app_date.strftime('%d/%m/%Y')} | Value: {app_val}")
            
            # User says for 06/02 appearance, play on 09/02 and 10/02 (4th and 5th day inclusive)
            # 06(1), 07(2), 08(3), 09(4), 10(5)
            target_day4 = app_date + timedelta(days=3)
            target_day5 = app_date + timedelta(days=4)
            
            print(f"Playing on: {target_day4.strftime('%d/%m/%Y')} and {target_day5.strftime('%d/%m/%Y')}")
            
            hit4 = test_df[test_df['date'] == target_day4]
            hit5 = test_df[test_df['date'] == target_day5]
            
            if not hit4.empty:
                print(f"Result 09/02: AK={hit4.iloc[0]['ak']}, LS2={hit4.iloc[0]['ls2']}")
            if not hit5.empty:
                print(f"Result 10/02: AK={hit5.iloc[0]['ak']}, LS2={hit5.iloc[0]['ls2']}")
                if int(hit5.iloc[0]['ls2']) == int(app_val):
                    print(">>> SUCCESS! 54 matched on 10/02 in LS2.")

    # Family/Mirror Logic
    family_map = {'0':'5', '1':'6', '2':'7', '3':'8', '4':'9', '5':'0', '6':'1', '7':'2', '8':'3', '9':'4'}
    def get_mirrors(n):
        s = f"{int(n):02d}"
        f1, f2 = family_map[s[0]], family_map[s[1]]
        return [int(s), int(f1+s[1]), int(s[0]+f2), int(f1+f2)]

    print("\n--- Running Improved Backtest (Mirror & Neighbor Logic) ---")
    results = {
        "Original": {"total": 0, "hits": 0},
        "With_Mirrors": {"total": 0, "hits": 0},
        "With_Neighbors": {"total": 0, "hits": 0},
        "3_to_6_Day_Window": {"total": 0, "hits": 0}
    }
    
    dates = df['date'].unique()
    for i in range(len(dates) - 20):
        base_row = df[df['date'] == dates[i]].iloc[0]
        ls1, ak = str(int(base_row['ls1'])).zfill(2), str(int(base_row['ak'])).zfill(2)
        digits = set(ls1) | set(ak)
        jodis = [int(d1+d2) for d1 in digits for d2 in digits]
        
        future = df[i+1:i+8]
        appearance = future[future['ak'].isin(jodis) | future['ls2'].isin(jodis)].head(1)
        
        if not appearance.empty:
            app_date = appearance.iloc[0]['date']
            app_val = int(appearance.iloc[0]['ak']) if int(appearance.iloc[0]['ak']) in jodis else int(appearance.iloc[0]['ls2'])
            
            # Different strategies
            targets_orig = [app_val]
            targets_mirrors = get_mirrors(app_val)
            targets_neighbors = [app_val, app_val-1, app_val+1, (app_val-10)%100, (app_val+10)%100]
            
            # Check windows
            window_45 = [app_date + timedelta(days=d) for d in [3, 4]]
            window_36 = [app_date + timedelta(days=d) for d in [2, 3, 4, 5]]
            
            # Test Original
            for d in window_45:
                row = df[df['date'] == d]
                if not row.empty and (int(row.iloc[0]['ak']) in targets_orig or int(row.iloc[0]['ls2']) in targets_orig):
                    results["Original"]["hits"] += 1
                    break
            results["Original"]["total"] += 1
            
            # Test Mirrors
            for d in window_45:
                row = df[df['date'] == d]
                if not row.empty and (int(row.iloc[0]['ak']) in targets_mirrors or int(row.iloc[0]['ls2']) in targets_mirrors):
                    results["With_Mirrors"]["hits"] += 1
                    break
            results["With_Mirrors"]["total"] += 1

            # Test Neighbors
            for d in window_45:
                row = df[df['date'] == d]
                if not row.empty and (int(row.iloc[0]['ak']) in targets_neighbors or int(row.iloc[0]['ls2']) in targets_neighbors):
                    results["With_Neighbors"]["hits"] += 1
                    break
            results["With_Neighbors"]["total"] += 1

            # Test Window 3-6
            for d in window_36:
                row = df[df['date'] == d]
                if not row.empty and (int(row.iloc[0]['ak']) in targets_orig or int(row.iloc[0]['ls2']) in targets_orig):
                    results["3_to_6_Day_Window"]["hits"] += 1
                    break
            results["3_to_6_Day_Window"]["total"] += 1

    def get_full_family(n):
        s = f"{int(n):02d}"
        d1, d2 = s[0], s[1]
        m1, m2 = family_map[d1], family_map[d2]
        # Full family: Original, Mirror1, Mirror2, Both Mirrors
        return [int(d1+d2), int(m1+d2), int(d1+m2), int(m1+m2)]

    print("\n--- Running Super Hybrid Backtest (Full Family & Day Analysis) ---")
    results = {
        "Full_Family": {"total": 0, "hits": 0, "days": {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}},
        "Original": {"total": 0, "hits": 0}
    }
    
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    dates = df['date'].unique()
    for i in range(len(dates) - 20):
        base_row = df[df['date'] == dates[i]].iloc[0]
        ls1, ak = str(int(base_row['ls1'])).zfill(2), str(int(base_row['ak'])).zfill(2)
        digits = set(ls1) | set(ak)
        jodis = [int(d1+d2) for d1 in digits for d2 in digits]
        
        future = df[i+1:i+8]
        appearance = future[future['ak'].isin(jodis) | future['ls2'].isin(jodis)].head(1)
        
        if not appearance.empty:
            app_date = appearance.iloc[0]['date']
            app_val = int(appearance.iloc[0]['ak']) if int(appearance.iloc[0]['ak']) in jodis else int(appearance.iloc[0]['ls2'])
            
            targets_family = get_full_family(app_val)
            window_45 = [app_date + timedelta(days=d) for d in [3, 4]]
            
            # Test Full Family
            hit_found = False
            for d in window_45:
                row = df[df['date'] == d]
                if not row.empty:
                    if int(row.iloc[0]['ak']) in targets_family or int(row.iloc[0]['ls2']) in targets_family:
                        results["Full_Family"]["hits"] += 1
                        results["Full_Family"]["days"][d.dayofweek] += 1
                        hit_found = True
                        break
            results["Full_Family"]["total"] += 1

    # Print Results
    ff = results["Full_Family"]
    acc = (ff['hits']/ff['total'])*100 if ff['total'] > 0 else 0
    print(f"Strategy: Full Family (4 Nos) | Hits: {ff['hits']} | Total: {ff['total']} | Accuracy: {acc:.2f}%")
    
    print("\n--- Best Days for this Trick (Hits by Day) ---")
    for d_idx, count in ff['days'].items():
        print(f"{day_names[d_idx]}: {count} hits")

if __name__ == "__main__":
    test_user_trick()
