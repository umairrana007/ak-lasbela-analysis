import json
from datetime import datetime, timedelta

def analyze_location_hot_joris():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # Analyze last 365 days
    last_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d')
    start_date = last_date - timedelta(days=365)
    recent_records = [r for r in records if datetime.strptime(r['date'], '%Y-%m-%d') >= start_date]

    location_stats = {k: {} for k in draw_keys}

    for record in recent_records:
        for k in draw_keys:
            val = record.get(k)
            if val and val != '--' and val != '??':
                v = str(val).zfill(2)
                location_stats[k][v] = location_stats[k].get(v, 0) + 1

    print("Location-Wise Hot Joris (Annual):")
    for k in draw_keys:
        sorted_loc = sorted(location_stats[k].items(), key=lambda x: x[1], reverse=True)
        print(f"  {k.upper()}: {sorted_loc[:5]}")

if __name__ == "__main__":
    analyze_location_hot_joris()
