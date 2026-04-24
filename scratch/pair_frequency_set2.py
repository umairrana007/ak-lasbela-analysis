import json

def analyze_pair_frequency_set2():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    target_digits = {'1', '3', '6', '7', '8'}
    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']

    pair_counts = {}

    for record in records:
        for k in draw_keys:
            val = record.get(k)
            if not val or val == '--' or val == '??':
                continue
            val_str = str(val).zfill(2)
            if all(d in target_digits for d in val_str):
                pair_counts[val_str] = pair_counts.get(val_str, 0) + 1

    # Sort by frequency
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)

    print("Top Frequencies for set {1, 3, 6, 7, 8}:")
    for pair, count in sorted_pairs[:10]:
        print(f"  {pair}: {count} hits")

if __name__ == "__main__":
    analyze_pair_frequency_set2()
