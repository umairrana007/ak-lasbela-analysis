import json

def analyze_location_correlations():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    target_digits = {'2', '0', '4', '9', '5'}
    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']

    def is_target_pair(val):
        if not val or val == '--' or val == '??':
            return False
        val_str = str(val).zfill(2)
        return all(d in target_digits for d in val_str)

    # Sort records by date ascending
    records.sort(key=lambda x: x['date'])

    same_day_correlations = {k: {k2: 0 for k2 in draw_keys} for k in draw_keys}
    next_day_correlations = {k: {k2: 0 for k2 in draw_keys} for k in draw_keys}
    source_counts = {k: 0 for k in draw_keys}

    for i in range(len(records)):
        record = records[i]
        
        # Find all hits in this day
        day_hits = [k for k in draw_keys if is_target_pair(record.get(k))]
        
        if not day_hits:
            continue

        # For each hit, check follow-ups
        for idx, source in enumerate(day_hits):
            source_counts[source] += 1
            
            # Same Day Follow-ups (after the source)
            for follow_up in day_hits[idx+1:]:
                same_day_correlations[source][follow_up] += 1
            
            # Next Day Follow-ups
            if i < len(records) - 1:
                next_record = records[i+1]
                for follow_up in draw_keys:
                    if is_target_pair(next_record.get(follow_up)):
                        next_day_correlations[source][follow_up] += 1

    print("--- SAME DAY CORRELATIONS ---")
    for src in draw_keys:
        total = source_counts[src]
        if total == 0: continue
        print(f"If {src.upper()} hits:")
        for target in draw_keys:
            count = same_day_correlations[src][target]
            if count > 0:
                pct = (count / total) * 100
                print(f"  -> {target.upper()} (Same Day): {pct:.1f}% ({count}/{total})")

    print("\n--- NEXT DAY CORRELATIONS ---")
    for src in draw_keys:
        total = source_counts[src]
        if total == 0: continue
        print(f"If {src.upper()} hits today:")
        for target in draw_keys:
            count = next_day_correlations[src][target]
            if count > 0:
                pct = (count / total) * 100
                print(f"  -> {target.upper()} (Next Day): {pct:.1f}% ({count}/{total})")

if __name__ == "__main__":
    analyze_location_correlations()
