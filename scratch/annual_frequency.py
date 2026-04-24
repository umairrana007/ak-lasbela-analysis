import json
from datetime import datetime, timedelta

def analyze_annual_frequency():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    records.sort(key=lambda x: x['date'])

    # Filter last 365 days
    last_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d')
    start_date = last_date - timedelta(days=365)
    annual_records = [r for r in records if datetime.strptime(r['date'], '%Y-%m-%d') >= start_date]

    pair_counts = {str(i).zfill(2): 0 for i in range(100)}

    for record in annual_records:
        for k in draw_keys:
            val = record.get(k)
            if val and val != '--' and val != '??':
                val_str = str(val).zfill(2)
                if val_str in pair_counts:
                    pair_counts[val_str] += 1

    counts = list(pair_counts.values())
    avg_hits = sum(counts) / 100
    max_hits = max(counts)
    min_hits = min(counts)

    # Find top 5 and bottom 5
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"Annual Analysis (Last 365 Days, {len(annual_records)} days):")
    print(f"Average hits per jori: {avg_hits:.2f}")
    print(f"Maximum hits: {max_hits} (Jori: {sorted_pairs[0][0]})")
    print(f"Minimum hits: {min_hits}")
    
    print("\nTop 5 Most Frequent Joriyaan (Yearly):")
    for p, c in sorted_pairs[:5]:
        print(f"  {p}: {c} hits")

if __name__ == "__main__":
    analyze_annual_frequency()
