import json
from datetime import datetime, timedelta

def get_today_hot_jodi():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # 1. Last 30 days frequency (to see what is 'Hot' recently)
    last_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d')
    start_date = last_date - timedelta(days=30)
    recent_records = [r for r in records if datetime.strptime(r['date'], '%Y-%m-%d') >= start_date]
    
    recent_counts = {}
    for record in recent_records:
        for k in draw_keys:
            val = record.get(k)
            if val and val != '--' and val != '??':
                v = str(val).zfill(2)
                recent_counts[v] = recent_counts.get(v, 0) + 1

    # 2. Filter for Set 1 and Cross-Set (Current Active Patterns)
    set1 = {'2', '0', '4', '9', '5'}
    set2 = {'1', '3', '6', '7', '8'}
    
    hot_set1 = []
    hot_cross = []
    
    for pair, count in recent_counts.items():
        d1, d2 = pair[0], pair[1]
        if d1 in set1 and d2 in set1:
            hot_set1.append((pair, count))
        elif (d1 in set1 and d2 in set2) or (d1 in set2 and d2 in set1):
            hot_cross.append((pair, count))

    hot_set1.sort(key=lambda x: x[1], reverse=True)
    hot_cross.sort(key=lambda x: x[1], reverse=True)

    print("Hottest Joris in Last 30 Days:")
    print("Set 1 (Hot):", hot_set1[:5])
    print("Cross-Set (Hot):", hot_cross[:5])

if __name__ == "__main__":
    get_today_hot_jodi()
