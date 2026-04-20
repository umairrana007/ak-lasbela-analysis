import json
import os

def deduplicate():
    json_path = 'backend/records_cleaned.json'
    output_path = 'backend/records_to_upload.json'
    
    if not os.path.exists(json_path):
        print(f"File {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Deduplicate by date
    unique_records = {}
    for r in data:
        unique_records[r['date']] = r
    
    # Filter out known existing records in Firestore (based on my previous check)
    existing_dates = {
        '2025-01-01',
        '2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05',
        '2026-01-06', '2026-01-07', '2026-01-08', '2026-01-09', '2026-01-10',
        '2026-12-22', '2026-12-23', '2026-12-24', '2026-12-25', '2026-12-26',
        '2026-12-27', '2026-12-28', '2026-12-29', '2026-12-30', '2026-12-31'
    }
    
    records_to_upload = [r for date, r in unique_records.items() if date not in existing_dates]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(records_to_upload, f, indent=2)
    
    print(f"Total records: {len(data)}")
    print(f"Unique records: {len(unique_records)}")
    print(f"Records to upload: {len(records_to_upload)}")

if __name__ == "__main__":
    deduplicate()
