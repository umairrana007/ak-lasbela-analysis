import pandas as pd
import re
import os

def parse_records():
    file_path = 'Records.txt'
    if not os.path.exists(file_path):
        return []
    
    records = []
    current_year = 2025
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if "2026" in line: current_year = 2026
            if "2025" in line: current_year = 2025
            
            # Match date, numbers, and day
            match = re.search(r'(\d{2}/\d{2})\.+([\d\.]+)\.+(\w+)', line)
            if match:
                nums = [n.zfill(2) for n in match.group(2).split('.') if n]
                if len(nums) == 5:
                    records.append({
                        "date": f"{match.group(1)}/{current_year}",
                        "nums": nums
                    })
    return records

def analyze_logic():
    data = parse_records()
    if not data:
        print("No records parsed from Records.txt!")
        return

    rules = [
        (['21','12'], ['04','40']),
        (['02','20'], ['14','41']),
        (['03','30'], ['19','91','69','96']),
        (['01','10'], ['34','43','47','74']),
        (['18','81'], ['69','96']),
        (['32','29'], ['07','70']),
        (['75','57'], ['16','61']),
        (['73','37'], ['07','70','33','32']),
        (['54','45'], ['09','90','40','04']),
        (['44'], ['13','31']),
        (['56','65'], ['83','38','88']),
        (['13','31'], ['64','46','96','69','49','94']),
        (['42','24'], ['08','80','62','26']),
        (['35','52'], ['07','70','57','75']),
        (['02','20'], ['39','93']),
        (['06','60'], ['34','43','58','85']),
        (['05','50'], ['39','93']),
        (['35','53'], ['03','30','08','80']),
    ]

    print(f"--- Analysis Report (Total Records: {len(data)}) ---")
    print(f"{'Trigger':<15} | {'Target':<25} | {'Hits':<5} | {'Success':<7} | {'Accuracy'}")
    print("-" * 80)

    for triggers, targets in rules:
        total_occurrences = 0
        success_hits = 0
        
        triggers = [t.zfill(2) for t in triggers]
        targets = [t.zfill(2) for t in targets]

        for i in range(len(data) - 10):
            # Check if trigger in current row
            if any(t in data[i]['nums'] for t in triggers):
                total_occurrences += 1
                # Check next 10 rows
                hit = False
                for j in range(i + 1, i + 11):
                    if any(t in data[j]['nums'] for t in targets):
                        hit = True
                        break
                if hit:
                    success_hits += 1

        acc = (success_hits / total_occurrences * 100) if total_occurrences > 0 else 0
        print(f"{','.join(triggers):<15} | {','.join(targets):<25} | {total_occurrences:<5} | {success_hits:<7} | {acc:.1f}%")

if __name__ == "__main__":
    analyze_logic()
