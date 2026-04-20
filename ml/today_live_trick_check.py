import pandas as pd
from datetime import datetime, timedelta

def find_today_opportunities():
    df = pd.read_csv('ml/processed_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    target_date = datetime(2026, 4, 20)
    # 4th day window: Appearance must be on 17/04
    # 5th day window: Appearance must be on 16/04
    appearance_dates = [target_date - timedelta(days=3), target_date - timedelta(days=4)]
    
    print(f"--- Scanning for Today's Opportunities ({target_date.strftime('%d/%m/%Y')}) ---")
    
    opportunities = []
    
    for app_date in appearance_dates:
        app_row = df[df['date'] == app_date]
        if app_row.empty: continue
        
        # Check all possible base dates in the last 60 days before this appearance
        for i in range(len(df)):
            base_date = df.iloc[i]['date']
            if base_date >= app_date: break
            if base_date < app_date - timedelta(days=60): continue
            
            ls1 = str(int(df.iloc[i]['ls1'])).zfill(2)
            ak = str(int(df.iloc[i]['ak'])).zfill(2)
            digits = set(ls1) | set(ak)
            jodis = [int(d1+d2) for d1 in digits for d2 in digits]
            
            # Did any of these jodis appear on app_date in AK or LS2?
            ak_val = int(app_row.iloc[0]['ak'])
            ls2_val = int(app_row.iloc[0]['ls2'])
            
            if ak_val in jodis:
                opportunities.append({
                    "base_date": base_date,
                    "app_date": app_date,
                    "value": ak_val,
                    "center": "AK",
                    "window": "4th Day" if app_date == target_date - timedelta(days=3) else "5th Day"
                })
            if ls2_val in jodis:
                opportunities.append({
                    "base_date": base_date,
                    "app_date": app_date,
                    "value": ls2_val,
                    "center": "LS2",
                    "window": "4th Day" if app_date == target_date - timedelta(days=3) else "5th Day"
                })

    if not opportunities:
        print("No direct matches found based on the 4th/5th day cycle for today.")
    else:
        # Deduplicate and present
        seen = set()
        for op in opportunities:
            key = (op['value'], op['window'])
            if key not in seen:
                print(f"Match Found! Value: {op['value']} | Appeared on: {op['app_date'].strftime('%d/%m/%Y')} ({op['center']})")
                print(f"Logic: Derived from Base Date {op['base_date'].strftime('%d/%m/%Y')} (LS1/AK Cross-Match)")
                print(f"Target for Today: {op['value']} (and its Family: {get_full_family(op['value'])})")
                print("-" * 30)
                seen.add(key)

def get_full_family(n):
    family_map = {'0':'5', '1':'6', '2':'7', '3':'8', '4':'9', '5':'0', '6':'1', '7':'2', '8':'3', '9':'4'}
    s = f"{int(n):02d}"
    d1, d2 = s[0], s[1]
    m1, m2 = family_map[d1], family_map[d2]
    return sorted(list(set([int(d1+d2), int(m1+d2), int(d1+m2), int(m1+m2)])))

if __name__ == "__main__":
    find_today_opportunities()
