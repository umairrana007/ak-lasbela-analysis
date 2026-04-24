import json
import sys

# Set output encoding to UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_table():
    with open('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'r', encoding='utf-8') as f:
        records = json.load(f)

    target_digits = {'2', '0', '4', '9', '5'}
    draw_keys = ['gm', 'ls1', 'ak', 'ls2', 'ls3']

    def is_target_pair(val):
        if not val or val == '--' or val == '??':
            return False
        val_str = str(val).zfill(2)
        return all(d in target_digits for d in val_str)

    # Sort records by date ascending
    records.sort(key=lambda x: x['date'])

    table_data = []

    for i in range(len(records)):
        record = records[i]
        day_hits = [k for k in draw_keys if is_target_pair(record.get(k))]
        
        if day_hits:
            first_hit_key = day_hits[0]
            first_hit_val = record[first_hit_key]
            
            same_day_hits = []
            for k in day_hits[1:]:
                same_day_hits.append(f"{k.upper()}({record[k]})")
            
            next_day_hits = []
            if i < len(records) - 1:
                next_record = records[i+1]
                next_day_hits = [f"{k.upper()}({next_record[k]})" for k in draw_keys if is_target_pair(next_record.get(k))]

            # Full Record Column
            full_rec = f"{record.get('gm','--')}.{record.get('ls1','--')}.{record.get('ak','--')}.{record.get('ls2','--')}.{record.get('ls3','--')}"

            # Construct the descriptive sentence
            status_parts = []
            if same_day_hits:
                status_parts.append(f"Same Day per {', '.join(same_day_hits)} ayie hai")
            
            if next_day_hits:
                status_parts.append(f"or next day main {', '.join(next_day_hits)}")

            table_data.append({
                "date": record['date'],
                "day": record.get('day', '-'),
                "full_record": full_rec,
                "first_hit": f"{first_hit_key.upper()}({first_hit_val})",
                "follow_up": " ".join(status_parts) if status_parts else "No Follow-up"
            })

    # Filter by date range if needed, or just get the last 30
    # The user asked for "12-3-2026 se 4-9-2026", which is basically the whole period I was already showing.
    
    # Let's filter specifically for that range to be precise
    filtered_instances = [r for r in table_data if "2026-03-12" <= r['date'] <= "2026-04-23"]

    print("| Date | Day | Full Record (GM.LS1.AK.LS2.LS3) | First Hit | Follow-up Status |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    for row in filtered_instances:
        print(f"| {row['date']} | {row['day']} | {row['full_record']} | {row['first_hit']} | {row['follow_up']} |")

if __name__ == "__main__":
    generate_table()
