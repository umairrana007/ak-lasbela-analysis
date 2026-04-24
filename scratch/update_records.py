import json

def add_new_records():
    file_path = 'c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    new_entries = [
        {"date": "2026-04-20", "gm": "98", "ls1": "50", "ak": "88", "ls2": "81", "ls3": "90", "day": "Mon"},
        {"date": "2026-04-21", "gm": "42", "ls1": "25", "ak": "84", "ls2": "97", "ls3": "35", "day": "Tue"},
        {"date": "2026-04-22", "gm": "09", "ls1": "52", "ak": "41", "ls2": "69", "ls3": "76", "day": "Wed"},
        {"date": "2026-04-23", "gm": "09", "ls1": "84", "ak": "51", "ls2": "19", "ls3": "37", "day": "Thur"}
    ]

    # Avoid duplicates
    existing_dates = {r['date'] for r in records}
    added_count = 0
    for entry in new_entries:
        if entry['date'] not in existing_dates:
            records.append(entry)
            added_count += 1

    # Sort by date
    records.sort(key=lambda x: x['date'])

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=4)
    
    print(f"Added {added_count} new records.")

if __name__ == "__main__":
    add_new_records()
