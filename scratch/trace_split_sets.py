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
    records_path = r'c:\Users\Muhammad.Umair\Desktop\Lottery_Pattern_Pro\public\Records.txt'
    with open(records_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        p = parse_line(line)
        if p: records.append(p)

    # Filter records from 28/02 onwards
    start_index = -1
    for i, r in enumerate(records):
        if r['date'] == '28/02':
            start_index = i
            break
    
    if start_index == -1: return

    target_range = records[start_index:] # From 28/02 to the end (19/04)

    print(f"{'BASE DATE':<10} | {'SET TYPE':<10} | {'TARGET':<5} | {'HIT DATE':<15} | {'HIT DRAW':<10} | {'RESULT'}")
    print("-" * 85)

    for i in range(len(target_range)):
        base_r = target_range[i]
        
        # Calculate the 4 Split Sets for this base day
        # Group 1: GM, LS1, AK
        set_a = set(base_r['gm'] + base_r['ak'][0])
        set_b = set(base_r['ls1'] + base_r['ak'][1])
        # Group 2: AK, LS2, LS3
        set_c = set(base_r['ak'] + base_r['ls3'][0])
        set_d = set(base_r['ls2'] + base_r['ls3'][1])
        
        sets_to_find = [
            {'digits': set_a, 'label': 'Set A', 'val': base_r['gm'] + base_r['ak'][0]},
            {'digits': set_b, 'label': 'Set B', 'val': base_r['ls1'] + base_r['ak'][1]},
            {'digits': set_c, 'label': 'Set C', 'val': base_r['ak'] + base_r['ls3'][0]},
            {'digits': set_d, 'label': 'Set D', 'val': base_r['ls2'] + base_r['ls3'][1]}
        ]

        # Search for these sets in subsequent days (starting from base_day + 1)
        # Search all records in history, not just target_range
        base_global_idx = records.index(base_r)
        
        for target in sets_to_find:
            hit_found = False
            # Scan forward in the entire record set
            for j in range(base_global_idx + 1, len(records) - 1):
                curr = records[j]
                nxt = records[j+1]
                draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
                
                for d in draws:
                    # Check Thandel: Current Jodi + Next Day Open or Close
                    if set(curr[d] + nxt[d][0]) == target['digits'] or set(curr[d] + nxt[d][1]) == target['digits']:
                        hit_val = curr[d] + nxt[d][0] if set(curr[d] + nxt[d][0]) == target['digits'] else curr[d] + nxt[d][1]
                        print(f"{base_r['date']:<10} | {target['label']:<10} | {target['val']:<5} | {curr['date']}->{nxt['date']:<8} | {d.upper():<10} | {hit_val}")
                        hit_found = True
                        break
                if hit_found: break
            
            if not hit_found:
                print(f"{base_r['date']:<10} | {target['label']:<10} | {target['val']:<5} | {'PENDING':<15} | {'-':<10} | -")

analyze()
