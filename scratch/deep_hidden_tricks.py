import re

def parse_records():
    records = []
    # Use latin-1 or similar to avoid decoding errors
    with open('Records.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # Use regex to find all 2-digit numbers in the line
            # Date part is usually DD/MM
            date_match = re.search(r'(\d{2}/\d{2})', line)
            if not date_match: continue
            
            date_str = date_match.group(1)
            
            # Find all 2-digit numbers after the date
            numbers = re.findall(r'\.(\d{2})', line)
            if not numbers:
                # Try finding numbers separated by anything non-digit
                parts = re.split(r'[^0-9]', line)
                numbers = [p for p in parts if len(p) == 2 and p.isdigit()]
                # Remove the date parts from the start
                if len(numbers) >= 7: # DD, MM, GM, LS1, AK, LS2, LS3
                    numbers = numbers[2:7]
                elif len(numbers) >= 5:
                    numbers = numbers[:5]
                else:
                    continue
            
            # Find the day name (usually at the end)
            day_match = re.search(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Tues|Thur|𝐅𝐫𝐢)', line, re.I)
            day = day_match.group(1) if day_match else "Unknown"
            
            if len(numbers) >= 5:
                records.append({
                    'date': date_str,
                    'gm': numbers[0], 'ls1': numbers[1], 'ak': numbers[2],
                    'ls2': numbers[3], 'ls3': numbers[4],
                    'day': day,
                    'raw': numbers[:5]
                })
    return records

def check_target_overlap(day_records):
    # Digits for 71.20.59 target system
    master_digits = {'7', '1', '2', '0', '5', '9'}
    
    fired_targets = []
    raw = day_records['raw']
    for i in range(len(raw)-1):
        combined = raw[i] + raw[i+1]
        digits = set(combined)
        # Target if it uses our master digits and has at least 2 distinct digits
        if digits.issubset(master_digits) and len(digits) >= 2:
            fired_targets.append(combined)
            
    return fired_targets

def analyze():
    records = parse_records()
    if not records:
        print("Error: No records parsed. Check the format.")
        return
        
    print(f"Analyzing {len(records)} records...")
    
    jora_success = 0
    total_multi_triggers = 0
    
    for i in range(len(records) - 4):
        targets = check_target_overlap(records[i])
        
        # Hidden Trick: Multiple Targets -> Double (Jora)
        if len(targets) >= 2:
            total_multi_triggers += 1
            
            found_jora = False
            for j in range(1, 4): # Check next 3 days
                next_day = records[i+j]
                for val in next_day['raw']:
                    if val[0] == val[1]:
                        found_jora = True
                        break
                if found_jora: break
            
            if found_jora:
                jora_success += 1

    print(f"\n--- [HIDDEN TRICK: THE DOUBLE JORA RULE] ---")
    print(f"Days with 2+ Targets fired: {total_multi_triggers}")
    print(f"Doubles hit in next 3 days: {jora_success}")
    if total_multi_triggers > 0:
        rate = (jora_success/total_multi_triggers)*100
        print(f"Success Rate: {rate:.2f}%")
        if rate > 70:
            print(">>> VALIDATED: Common Overlap leads to Doubles!")

    # Weekend Dump Analysis
    day_stats = {}
    for r in records:
        day = r['day'][:3].capitalize() # Normalize Mon, Tue, etc.
        if day == "Tues": day = "Tue"
        if day == "Thur": day = "Thu"
        if day == "𝐅𝐫𝐢": day = "Fri"
        
        doubles = len([g for g in r['raw'] if g[0] == g[1]])
        if day not in day_stats:
            day_stats[day] = {'hits': 0, 'count': 0}
        day_stats[day]['hits'] += doubles
        day_stats[day]['count'] += 1
            
    print(f"\n--- [HIDDEN TRICK: WEEKEND DUMP (Average Doubles per Day)] ---")
    sorted_days = sorted(day_stats.items(), key=lambda x: x[1]['hits']/x[1]['count'] if x[1]['count'] > 0 else 0, reverse=True)
    for day, stat in sorted_days:
        avg = stat['hits']/stat['count']
        print(f"{day}: {avg:.2f} doubles/day")

if __name__ == "__main__":
    analyze()
