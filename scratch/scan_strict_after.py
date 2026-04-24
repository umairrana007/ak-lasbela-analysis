import re
from datetime import datetime

def parse_line(line):
    match = re.search(r'(\d{2}/\d{2})\.\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.\.(\w+)', line)
    if match:
        # Assuming year 2026 for comparison
        dt = datetime.strptime(match.group(1) + "/2026", "%d/%m/%Y")
        return {
            'dt': dt,
            'date_str': match.group(1),
            'gm': match.group(2), 'ls1': match.group(3), 'ak': match.group(4), 'ls2': match.group(5), 'ls3': match.group(6),
            'day': match.group(7), 'raw': line.strip()
        }
    return None

def analyze():
    records_path = r'c:\Users\Muhammad.Umair\Desktop\akwebapp\Records.txt'
    with open(records_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        p = parse_line(line)
        if p: records.append(p)

    # Cutoff date: 08/03/2026
    cutoff = datetime(2026, 3, 8)

    target_sets = [
        {'digits': set('671'), 'label': '671'},
        {'digits': set('674'), 'label': '674'},
        {'digits': set('672'), 'label': '672'},
        {'digits': set('679'), 'label': '679'},
        {'digits': set('293'), 'label': '293'},
        {'digits': set('290'), 'label': '290'},
        {'digits': set('297'), 'label': '297'},
        {'digits': set('292'), 'label': '292'},
    ]

    print(f"--- STRICT HITS AFTER 08/03/2026 ---")
    print(f"{'DATE':<10} | {'DAY':<10} | {'TYPE':<25} | {'MATCH':<5} | {'SET':<10}")
    print("-" * 75)

    for i in range(len(records)):
        r = records[i]
        if r['dt'] <= cutoff:
            continue
        
        # Horizontal
        h_combos = [
            {'val': r['gm'] + r['ls1'][0], 'type': 'GM_Jodi + LS1_Open'},
            {'val': r['gm'] + r['ak'][0],  'type': 'GM_Jodi + AK_Open'},
            {'val': r['ls1'] + r['ak'][0], 'type': 'LS1_Jodi + AK_Open'},
            {'val': r['ak'] + r['ls2'][0], 'type': 'AK_Jodi + LS2_Open'},
            {'val': r['gm'][1] + r['ls1'], 'type': 'GM_Close + LS1_Jodi'},
            {'val': r['ak'][1] + r['ls2'], 'type': 'AK_Close + LS2_Jodi'},
        ]
        for combo in h_combos:
            for t in target_sets:
                if set(combo['val']) == t['digits']:
                    print(f"{r['date_str']:<10} | {r['day']:<10} | {combo['type']:<25} | {combo['val']:<5} | {t['label']:<10}")

        # Vertical
        if i < len(records) - 1:
            nxt = records[i+1]
            draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
            for d in draws:
                v_open = r[d] + nxt[d][0]
                v_close = r[d] + nxt[d][1]
                for t in target_sets:
                    if set(v_open) == t['digits'] or set(v_close) == t['digits']:
                        res = v_open if set(v_open) == t['digits'] else v_close
                        print(f"{r['date_str']:<10} | {r['day']:<10} | {d.upper() + '_Vertical':<25} | {res:<5} | {t['label']:<10}")

analyze()
