import re

def parse_records():
    records = []
    with open('Records.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            date_match = re.search(r'(\d{2}/\d{2})', line)
            if not date_match: continue
            
            parts = re.split(r'[^0-9]', line)
            numbers = [p for p in parts if len(p) == 2 and p.isdigit()]
            if len(numbers) >= 7: numbers = numbers[2:7]
            elif len(numbers) >= 5: numbers = numbers[:5]
            else: continue
            
            if len(numbers) >= 5:
                records.append({'date': date_match.group(1), 'raw': numbers[:5]})
    return records

def analyze_missing_digit():
    records = parse_records()
    # 3-digit Targets from Line 1
    targets = [
        ('712', '059'), ('710', '259'), ('715', '209'), ('719', '205'),
        ('120', '759'), ('105', '927'), ('109', '527'), ('207', '159'),
        ('907', '125'), ('507', '129')
    ]
    
    total_partial_triggers = 0
    missing_digit_success = 0
    
    for i in range(len(records) - 7):
        day_nums = "".join(records[i]['raw'])
        day_digits = set(day_nums)
        
        for target_str, counterpart in targets:
            target_digits = set(target_str)
            # Find if exactly 2 digits from target are present
            intersect = target_digits.intersection(day_digits)
            if len(intersect) == 2:
                missing = (target_digits - intersect).pop()
                total_partial_triggers += 1
                
                # Check next 7 days for hits containing the missing digit
                found = False
                for j in range(1, 8):
                    next_day_nums = "".join(records[i+j]['raw'])
                    if missing in next_day_nums:
                        found = True
                        break
                if found:
                    missing_digit_success += 1
                    
    print(f"\n--- [HIDDEN TRICK: THE MISSING DIGIT RULE] ---")
    print(f"Partial Triggers Found (2/3 digits): {total_partial_triggers}")
    print(f"Missing Digit appeared in next 7 days: {missing_digit_success}")
    if total_partial_triggers > 0:
        print(f"Success Rate: {(missing_digit_success/total_partial_triggers)*100:.2f}%")

if __name__ == "__main__":
    analyze_missing_digit()
