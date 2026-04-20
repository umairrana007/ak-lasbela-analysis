import re
import json
from datetime import datetime

def convert_records_to_json(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    records = []
    current_year = 2025 # Default
    
    for line in lines:
        if "2026" in line:
            current_year = 2026
        
        # Match pattern: 01/01..61.46.61.47.64..Wed
        match = re.search(r'(\d{2}/\d{2})\.\.([\d\.]+)\.\.(\w+)', line)
        if match:
            date_short = match.group(1)
            numbers_part = match.group(2)
            day = match.group(3)
            
            day_month = date_short.split('/')
            full_date = f"{current_year}-{day_month[1]}-{day_month[0]}"
            
            numbers = numbers_part.split('.')
            numbers = [n for n in numbers if n]
            
            if len(numbers) == 5:
                record = {
                    "date": full_date,
                    "display_date": date_short,
                    "gm": numbers[0],
                    "ls1": numbers[1],
                    "ak": numbers[2],
                    "ls2": numbers[3],
                    "ls3": numbers[4],
                    "day": day,
                    "source": "historical"
                }
                records.append(record)
                
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
    print(f"Converted {len(records)} records to {output_path}")

if __name__ == "__main__":
    convert_records_to_json('Records.txt', 'backend/records_cleaned.json')
