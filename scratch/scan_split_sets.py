import re

def parse_line(line):
    # Standard parser for the record lines
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

    # Base Data from 28-02: 71.20.59.57.66
    # Group 1 (GM, LS1, AK): 71, 20, 59
    # Set A: 71 + 5 = 715
    # Set B: 20 + 9 = 209
    
    # Group 2 (AK, LS2, LS3): 59, 57, 66
    # Set C: 59 + 6 = 596
    # Set D: 57 + 6 = 576
    
    targets = [
        {'digits': set('715'), 'label': 'Set A (715)'},
        {'digits': set('209'), 'label': 'Set B (209)'},
        {'digits': set('596'), 'label': 'Set C (596)'},
        {'digits': set('576'), 'label': 'Set D (576)'}
    ]

    print(f"{'DATE RANGE':<18} | {'SET TYPE':<12} | {'HIT SET':<5} | {'COMPLETE RECORD':<30} | {'DAY'}")
    print("-" * 100)

    for i in range(len(records) - 1):
        r_current = records[i]
        r_next = records[i+1]
        
        draws = ['gm', 'ls1', 'ak', 'ls2', 'ls3']
        
        for d in draws:
            # A Thandel is Current Day Jodi + Next Day (any digit)
            # User says: "next one figure... Open ata yah close ata humay koi farq nahi parta"
            # So we check both digits of the next day.
            
            # Check Next Day Open
            thandel_open = r_current[d] + r_next[d][0]
            # Check Next Day Close
            thandel_close = r_current[d] + r_next[d][1]
            
            for target in targets:
                # Match Open Digit
                if set(thandel_open) == target['digits']:
                    date_range = f"{r_current['date']}->{r_next['date']}"
                    print(f"{date_range:<18} | {target['label']:<12} | {thandel_open:<5} | {r_current['raw']:<30} | {r_current['day']}")
                
                # Match Close Digit (if different from open)
                if r_next[d][0] != r_next[d][1]:
                    if set(thandel_close) == target['digits']:
                        date_range = f"{r_current['date']}->{r_next['date']}"
                        print(f"{date_range:<18} | {target['label']:<12} | {thandel_close:<5} | {r_current['raw']:<30} | {r_current['day']}")

analyze()
