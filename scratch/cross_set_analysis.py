import json

def analyze_cross_set_transitions():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    records.sort(key=lambda x: x['date'])

    set1 = {'2', '0', '4', '9', '5'}
    set2 = {'1', '3', '6', '7', '8'}

    def get_type(val):
        if not val or val == '--' or val == '??':
            return None
        v = str(val).zfill(2)
        d1, d2 = v[0], v[1]
        
        if d1 in set1 and d2 in set1: return "SET1"
        if d1 in set2 and d2 in set2: return "SET2"
        # Cross set is one from each
        if (d1 in set1 and d2 in set2) or (d1 in set2 and d2 in set1): return "CROSS"
        return "OTHER"

    stats = {
        "SET1": {"SET1": 0, "SET2": 0, "CROSS": 0, "OTHER": 0, "TOTAL": 0},
        "SET2": {"SET1": 0, "SET2": 0, "CROSS": 0, "OTHER": 0, "TOTAL": 0},
        "CROSS": {"SET1": 0, "SET2": 0, "CROSS": 0, "OTHER": 0, "TOTAL": 0}
    }

    for i in range(len(records) - 1):
        today = records[i]
        tomorrow = records[i+1]
        
        for k in draw_keys:
            type_today = get_type(today.get(k))
            type_tomorrow = get_type(tomorrow.get(k))
            
            if type_today in stats and type_tomorrow:
                stats[type_today][type_tomorrow] += 1
                stats[type_today]["TOTAL"] += 1

    print("--- TRANSITION ANALYSIS (Same Game, Next Day) ---")
    for start_type in ["SET1", "SET2", "CROSS"]:
        total = stats[start_type]["TOTAL"]
        if total == 0: continue
        print(f"If today is {start_type}:")
        for end_type in ["SET1", "SET2", "CROSS"]:
            count = stats[start_type][end_type]
            pct = (count / total) * 100
            print(f"  -> Tomorrow will be {end_type}: {pct:.1f}% ({count}/{total})")

if __name__ == "__main__":
    analyze_cross_set_transitions()
