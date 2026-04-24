import re

def parse_line(line):
    match = re.search(r'(\d{2}/\d{2})\.\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.\.(\w+)', line)
    if match:
        return {
            'date': match.group(1),
            'gm': match.group(2),
            'ls1': match.group(3),
            'ak': match.group(4),
            'ls2': match.group(5),
            'ls3': match.group(6),
            'day': match.group(7)
        }
    return None

def analyze():
    # Path to the shared records file
    records_path = r'c:\Users\Muhammad.Umair\Desktop\Lottery_Pattern_Pro\public\Records.txt'
    with open(records_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        p = parse_line(line)
        if p:
            records.append(p)

    target1 = set('725')
    target2 = set('109')

    print(f"--- Searching for Sets {target1} and {target2} ---")

    for i in range(len(records)):
        r = records[i]
        
        # Horizontal Check (First Digits of GM, LS1, AK)
        h1 = r['gm'][0] + r['ls1'][0] + r['ak'][0]
        h2 = r['gm'][1] + r['ls1'][1] + r['ak'][1]
        
        if set(h1) == target1 or set(h1) == target2:
            print(f"Match Found: Horizontal on {r['date']} ({r['day']}) -> {h1 if set(h1) in [target1, target2] else h2}")

        # Straight Line / Vertical (Thandel)
        if i < len(records) - 1:
            next_r = records[i+1]
            draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
            for d in draws:
                # Thandel Logic: Current Jodi + Next Day first digit of same draw
                thandel = r[d] + next_r[d][0]
                if set(thandel) == target1:
                    print(f"Match Found: Thandel Hit {target1} on {r['date']} -> {next_r['date']} in {d.upper()}: {thandel}")
                if set(thandel) == target2:
                    print(f"Match Found: Thandel Hit {target2} on {r['date']} -> {next_r['date']} in {d.upper()}: {thandel}")

analyze()
