import re

def parse_line(line):
    match = re.search(r'(\d{2}/\d{2})\.\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.(\d{2})\.\.(\w+)', line)
    if match:
        return {
            'date': match.group(1),
            'gm': match.group(2), 'ls1': match.group(3), 'ak': match.group(4), 'ls2': match.group(5), 'ls3': match.group(6),
            'day': match.group(7), 'raw': line.strip()
        }
    return None

def analyze():
    # Using the local Records.txt - User should ensure this file matches their actual data
    records_path = r'c:\Users\Muhammad.Umair\Desktop\akwebapp\Records.txt'
    with open(records_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        p = parse_line(line)
        if p: records.append(p)

    # User's provided sets for 08/03/2026 (Group 1 example: 671, 429, 674, 129, etc.)
    target_sets = [
        {'digits': set('671'), 'label': '671'},
        {'digits': set('429'), 'label': '429 (Rem)'},
        {'digits': set('674'), 'label': '674'},
        {'digits': set('129'), 'label': '129 (Rem)'},
        {'digits': set('293'), 'label': '293'},
        {'digits': set('072'), 'label': '072 (Rem)'}
    ]

    print(f"{'DATE':<10} | {'TYPE':<20} | {'MATCH':<5} | {'SET':<10} | {'FULL RECORD'}")
    print("-" * 110)

    for i in range(len(records)):
        r = records[i]
        
        # --- HORIZONTAL CHECKS (Same Day) ---
        # 1. Jodi + Open combinations
        h_combos = [
            {'val': r['gm'] + r['ls1'][0], 'type': 'GM_Jodi + LS1_Open'},
            {'val': r['gm'] + r['ak'][0],  'type': 'GM_Jodi + AK_Open'},
            {'val': r['ls1'] + r['ak'][0], 'type': 'LS1_Jodi + AK_Open'},
            {'val': r['ls1'] + r['ls2'][0], 'type': 'LS1_Jodi + LS2_Open'},
            {'val': r['ak'] + r['ls2'][0],  'type': 'AK_Jodi + LS2_Open'},
            {'val': r['ls2'] + r['ls3'][0], 'type': 'LS2_Jodi + LS3_Open'},
            
            # 2. Close + Jodi combinations
            {'val': r['gm'][1] + r['ls1'], 'type': 'GM_Close + LS1_Jodi'},
            {'val': r['gm'][1] + r['ak'],  'type': 'GM_Close + AK_Jodi'},
            {'val': r['ls1'][1] + r['ak'], 'type': 'LS1_Close + AK_Jodi'},
            {'val': r['ls1'][1] + r['ls2'], 'type': 'LS1_Close + LS2_Jodi'},
            {'val': r['ak'][1] + r['ls2'],  'type': 'AK_Close + LS2_Jodi'},
            {'val': r['ls2'][1] + r['ls3'], 'type': 'LS2_Close + LS3_Jodi'}
        ]

        for combo in h_combos:
            for t in target_sets:
                if set(combo['val']) == t['digits']:
                    print(f"{r['date']:<10} | {combo['type']:<20} | {combo['val']:<5} | {t['label']:<10} | {r['raw']}")

        # --- VERTICAL CHECKS (Next Day) ---
        if i < len(records) - 1:
            nxt = records[i+1]
            draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
            for d in draws:
                # Jodi + Next Day Open
                v_open = r[d] + nxt[d][0]
                # Jodi + Next Day Close
                v_close = r[d] + nxt[d][1]
                
                for t in target_sets:
                    if set(v_open) == t['digits']:
                        print(f"{r['date']:<10} | {d.upper() + '_Vertical (O)':<20} | {v_open:<5} | {t['label']:<10} | {r['raw']}")
                    elif set(v_close) == t['digits']:
                        print(f"{r['date']:<10} | {d.upper() + '_Vertical (C)':<20} | {v_close:<5} | {t['label']:<10} | {r['raw']}")

analyze()
