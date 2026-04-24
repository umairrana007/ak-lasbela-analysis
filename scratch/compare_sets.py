import json
from datetime import datetime, timedelta

def compare_sets():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    records.sort(key=lambda x: x['date'])

    # Filter last 90 days
    last_date = datetime.strptime(records[-1]['date'], '%Y-%m-%d')
    start_date = last_date - timedelta(days=90)
    recent_records = [r for r in records if datetime.strptime(r['date'], '%Y-%m-%d') >= start_date]

    set1 = {'2', '0', '4', '9', '5'}
    set2 = {'1', '3', '6', '7', '8'}

    def get_stats(target_digits, recs):
        hits_count = 0
        hit_days = []
        for r in recs:
            day_has_hit = False
            for k in draw_keys:
                val = r.get(k)
                if val and val != '--' and val != '??':
                    if all(d in target_digits for d in str(val).zfill(2)):
                        hits_count += 1
                        day_has_hit = True
            hit_days.append(day_has_hit)
        
        repeats = 0
        for i in range(len(hit_days) - 1):
            if hit_days[i] and hit_days[i+1]:
                repeats += 1
        
        total_hit_days = sum(hit_days)
        repeat_pct = (repeats / (total_hit_days - 1) * 100) if total_hit_days > 1 else 0
        return hits_count, total_hit_days, repeat_pct, hit_days

    s1_hits, s1_days, s1_repeat, s1_mask = get_stats(set1, recent_records)
    s2_hits, s2_days, s2_repeat, s2_mask = get_stats(set2, recent_records)

    # Check for "Switching" (Inverse correlation)
    both_hit = 0
    only_s1 = 0
    only_s2 = 0
    neither = 0
    for h1, h2 in zip(s1_mask, s2_mask):
        if h1 and h2: both_hit += 1
        elif h1: only_s1 += 1
        elif h2: only_s2 += 1
        else: neither += 1

    print(f"Comparison (Last 90 Days):")
    print(f"--- SET 1 {set1} ---")
    print(f"Total Hits: {s1_hits}")
    print(f"Days with at least one hit: {s1_days}")
    print(f"Repeat Chance (Next Day): {s1_repeat:.2f}%")
    
    print(f"\n--- SET 2 {set2} ---")
    print(f"Total Hits: {s2_hits}")
    print(f"Days with at least one hit: {s2_days}")
    print(f"Repeat Chance (Next Day): {s2_repeat:.2f}%")

    print(f"\n--- INTERACTION ---")
    print(f"Days BOTH hit: {both_hit}")
    print(f"Days ONLY SET 1 hit: {only_s1}")
    print(f"Days ONLY SET 2 hit: {only_s2}")
    print(f"Days NEITHER hit: {neither}")

if __name__ == "__main__":
    compare_sets()
