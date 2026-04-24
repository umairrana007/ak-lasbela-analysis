import json
from datetime import datetime, timedelta

def compare_lifetime_vs_annual():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # Lifetime counts
    lifetime_counts = {}
    for record in records:
        for k in draw_keys:
            val = record.get(k)
            if val and val != '--' and val != '??':
                v = str(val).zfill(2)
                lifetime_counts[v] = lifetime_counts.get(v, 0) + 1

    # Annual counts (last 365 days)
    last_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d')
    start_date = last_date - timedelta(days=365)
    annual_records = [r for r in records if datetime.strptime(r['date'], '%Y-%m-%d') >= start_date]
    
    annual_counts = {}
    for record in annual_records:
        for k in draw_keys:
            val = record.get(k)
            if val and val != '--' and val != '??':
                v = str(val).zfill(2)
                annual_counts[v] = annual_counts.get(v, 0) + 1

    print(f"Stats for Jori 08:")
    print(f"  Lifetime Hits (Since Jan 2025 - ~16 months): {lifetime_counts.get('08', 0)}")
    print(f"  Annual Hits (Last 12 months): {annual_counts.get('08', 0)}")
    
    print(f"\nStats for Jori 03:")
    print(f"  Lifetime Hits (Since Jan 2025 - ~16 months): {lifetime_counts.get('03', 0)}")
    print(f"  Annual Hits (Last 12 months): {annual_counts.get('03', 0)}")

if __name__ == "__main__":
    compare_lifetime_vs_annual()
