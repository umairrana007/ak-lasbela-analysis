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
            'day': match.group(7),
            'raw': line.strip()
        }
    return None

def analyze():
    records_path = r'c:\Users\Muhammad.Umair\Desktop\Lottery_Pattern_Pro\public\Records.txt'
    with open(records_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        p = parse_line(line)
        if p:
            records.append(p)

    # Base Targets from 28-02-2026: 71.20.59.57.66
    # Logic: [Draw A Close] + [Draw B Jodi]
    # Set 1: GM(1) + LS1(20) = 120
    # Set 2: LS1(0) + AK(59) = 059
    # Set 3: AK(9) + LS2(57) = 957
    # Set 4: LS2(7) + LS3(66) = 766
    
    base_sets = [
        {'digits': set('120'), 'name': 'GM_Close+LS1'},
        {'digits': set('059'), 'name': 'LS1_Close+AK'},
        {'digits': set('957'), 'name': 'AK_Close+LS2'},
        {'digits': set('766'), 'name': 'LS2_Close+LS3'}
    ]

    print(f"{'DATE':<10} | {'MATCH TYPE':<15} | {'SET':<5} | {'FULL RECORD':<30} | {'DAY'}")
    print("-" * 80)

    for i in range(len(records)):
        r = records[i]
        
        # 1. Check Horizontal Patterns on the same day
        h_sets = [
            r['gm'][1] + r['ls1'], # GM Close + LS1
            r['ls1'][1] + r['ak'], # LS1 Close + AK
            r['ak'][1] + r['ls2'], # AK Close + LS2
            r['ls2'][1] + r['ls3']  # LS2 Close + LS3
        ]
        
        for h_val in h_sets:
            for target in base_sets:
                if set(h_val) == target['digits']:
                    print(f"{r['date']:<10} | {'Horizontal':<15} | {h_val:<5} | {r['raw']:<30} | {r['day']}")

        # 2. Check Straight Line (Thandels)
        # Logic: [Current Jodi] + [Next Day First Digit]
        if i < len(records) - 1:
            next_r = records[i+1]
            draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
            for d in draws:
                thandel = r[d] + next_r[d][0]
                for target in base_sets:
                    if set(thandel) == target['digits']:
                        print(f"{r['date']:<10} | {d.upper() + ' Thandel':<15} | {thandel:<5} | {r['raw']:<30} | {r['day']}")

analyze()
