import csv
import json
import os
from datetime import datetime

def parse_complete_data():
    txt_path = 'c:/Users/Muhammad.Umair/Desktop/akwebapp/2023-2024-2025-2026 complete data.txt'
    json_path = 'c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json'
    
    if not os.path.exists(txt_path):
        print(f"Error: {txt_path} not found")
        return

    records = []
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        # Skip the header line
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row['date'].strip()
            # Handle special notes in the GM field (like "Shab-e-Barat", "Eid-Day-Game-Off")
            # If the date part doesn't look like a date, we might have issues.
            # But the date part seems consistent: DD/MM/YYYY
            
            try:
                # Try parsing the date
                dt = datetime.strptime(date_str, '%d/%m/%Y')
                iso_date = dt.strftime('%Y-%m-%d')
                display_date = dt.strftime('%d-%m-%y')
                
                # Check if numbers are valid. If not, they might be special markers
                gm = row['GM'].strip()
                ls1 = row['LS1'].strip()
                ak = row['AK'].strip()
                ls2 = row['LS2'].strip()
                ls3 = row['LS3'].strip()
                day = row['day'].strip()
                
                # If GM is a string like "Shab-e-Barat", we might want to store it differently
                # or skip it if the website expects only numbers.
                # Looking at the previous JSON, it seems to only contain records with numbers.
                # However, let's see how the website handles it.
                # Usually, if it's not a number, it's a holiday.
                
                # Normalize numbers with leading zeros
                record = {
                    "date": iso_date,
                    "display_date": display_date,
                    "gm": gm.zfill(2) if gm.isdigit() else gm,
                    "ls1": ls1.zfill(2) if ls1.isdigit() else ls1,
                    "ak": ak.zfill(2) if ak.isdigit() else ak,
                    "ls2": ls2.zfill(2) if ls2.isdigit() else ls2,
                    "ls3": ls3.zfill(2) if ls3.isdigit() else ls3,
                    "day": day
                }
                
                records.append(record)
            except Exception as e:
                print(f"Skipping line with date {date_str}: {e}")

    # Sort by date
    records.sort(key=lambda x: x['date'])
    
    # Remove duplicates
    unique_records = []
    seen_dates = set()
    for r in records:
        if r['date'] not in seen_dates:
            unique_records.append(r)
            seen_dates.add(r['date'])

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(unique_records, f, indent=2)
    
    print(f"Successfully parsed {len(unique_records)} records into {json_path}")

if __name__ == "__main__":
    parse_complete_data()
