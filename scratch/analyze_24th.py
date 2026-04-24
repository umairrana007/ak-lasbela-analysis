import json

def analyze_24th_day_pattern():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    results_24th = []

    for record in records:
        date_str = record['date']
        # Extract day from YYYY-MM-DD
        day = date_str.split('-')[2]
        
        if day == '24':
            hits = []
            for k in draw_keys:
                val = record.get(k)
                if val and val != '--' and val != '??':
                    hits.append(str(val).zfill(2))
            
            results_24th.append({
                'date': date_str,
                'hits': hits
            })

    print(f"History of 24th Date Draws ({len(results_24th)} months found):")
    for r in results_24th:
        print(f"  {r['date']}: {' | '.join(r['hits'])}")

    # Check frequency of hits on 24th
    all_hits = []
    for r in results_24th:
        all_hits.extend(r['hits'])
    
    from collections import Counter
    freq = Counter(all_hits)
    print("\nMost Frequent Joris on 24th Date:")
    for pair, count in freq.most_common(5):
        print(f"  {pair}: {count} times")

if __name__ == "__main__":
    analyze_24th_day_pattern()
