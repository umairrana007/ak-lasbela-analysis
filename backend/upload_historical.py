import firebase_admin
from firebase_admin import credentials, firestore
import re
from datetime import datetime
import os

def initialize_firebase():
    if not firebase_admin._apps:
        # Assuming we are running where default credentials or service account is configured
        # Or using the firebase-mcp-server's project context
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': 'ak-analysis-system-umair',
        })
    return firestore.client()

def upload_historical_records(file_path):
    db = initialize_firebase()
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    records = []
    current_year = 2025 # Based on the header in Records.txt
    
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
                    "timestamp": datetime.now().isoformat(),
                    "source": "historical"
                }
                records.append(record)
    
    print(f"Uploading {len(records)} records to Firestore...")
    batch = db.batch()
    count = 0
    for r in records:
        # Use date as ID to avoid duplicates
        doc_ref = db.collection('draws').document(r['date'])
        batch.set(doc_ref, r)
        count += 1
        
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Committed {count} records...")
            
    batch.commit()
    print(f"Successfully uploaded {count} historical records.")

if __name__ == "__main__":
    upload_historical_records('Records.txt')
