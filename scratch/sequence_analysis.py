import json

def analyze_sequences():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
    
    # Yesterday's hits
    yesterday = {
        'gm': '84',
        'ls1': '51',
        'ak': '19',
        'ls2': '37',
        'ls3': '35'
    }

    follow_ups = {k: [] for k in draw_keys}

    for i in range(len(records) - 1):
        for k in draw_keys:
            current_val = str(records[i].get(k)).zfill(2)
            if current_val == yesterday[k]:
                next_val = str(records[i+1].get(k)).zfill(2)
                if next_val != '??' and next_val != '--':
                    follow_ups[k].append(next_val)

    print("Sequence Analysis (What hits after yesterday's numbers in the same game):")
    for k in draw_keys:
        from collections import Counter
        c = Counter(follow_ups[k])
        print(f"  After {yesterday[k]} in {k.upper()}: {c.most_common(3)}")

if __name__ == "__main__":
    analyze_sequences()
