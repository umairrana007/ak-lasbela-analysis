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

def find_hit(target_digits, records, start_idx):
    for j in range(start_idx + 1, len(records) - 1):
        curr = records[j]
        nxt = records[j+1]
        draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
        for d in draws:
            if set(curr[d] + nxt[d][0]) == target_digits:
                return {'date': f"{curr['date']}->{nxt['date']}", 'draw': d.upper(), 'res': curr[d] + nxt[d][0], 'raw': curr['raw']}
            if nxt[d][0] != nxt[d][1]:
                if set(curr[d] + nxt[d][1]) == target_digits:
                    return {'date': f"{curr['date']}->{nxt['date']}", 'draw': d.upper(), 'res': curr[d] + nxt[d][1], 'raw': curr['raw']}
    return None

def analyze():
    records_path = r'c:\Users\Muhammad.Umair\Desktop\Lottery_Pattern_Pro\public\Records.txt'
    with open(records_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        p = parse_line(line)
        if p: records.append(p)

    start_index = -1
    for i, r in enumerate(records):
        if r['date'] == '28/02':
            start_index = i
            break
    
    if start_index == -1: return

    target_range = records[start_index:]

    print(f"{'BASE DATE':<10} | {'GROUP':<7} | {'SET 1 (HIT)':<12} | {'SET 2 (REM)':<12} | {'RECORDS (GM.LS1.AK.LS2.LS3)'}")
    print("-" * 120)

    for i in range(len(target_range)):
        base_r = target_range[i]
        base_idx = records.index(base_r)
        
        # Group 1 Logic
        sA_digits = set(base_r['gm'] + base_r['ak'][0])
        sB_digits = set(base_r['ls1'] + base_r['ak'][1])
        hA = find_hit(sA_digits, records, base_idx)
        hB = find_hit(sB_digits, records, base_idx)
        
        statusA = f"{hA['date']} ({hA['draw']})" if hA else "PENDING"
        statusB = f"{hB['date']} ({hB['draw']})" if hB else "PENDING"
        
        # Display Group 1
        print(f"{base_r['date']:<10} | {'G1':<7} | {statusA:<12} | {statusB:<12} | {base_r['gm']}.{base_r['ls1']}.{base_r['ak']}.{base_r['ls2']}.{base_r['ls3']}")

        # Group 2 Logic
        sC_digits = set(base_r['ak'] + base_r['ls3'][0])
        sD_digits = set(base_r['ls2'] + base_r['ls3'][1])
        hC = find_hit(sC_digits, records, base_idx)
        hD = find_hit(sD_digits, records, base_idx)
        
        statusC = f"{hC['date']} ({hC['draw']})" if hC else "PENDING"
        statusD = f"{hD['date']} ({hD['draw']})" if hD else "PENDING"
        
        # Display Group 2
        print(f"{' ':<10} | {'G2':<7} | {statusC:<12} | {statusD:<12} | {' (Same as above)':<30}")
        print("-" * 120)

analyze()
