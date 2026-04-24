import json
import os
from google.cloud import firestore

def sync_data():
    # Use the service account file present in the root
    key_file = 'c:/Users/Muhammad.Umair/Desktop/akwebapp/ak-analysis-system-umair-firebase-adminsdk-fbsvc-6eceff3ff0.json'
    
    if os.path.exists(key_file):
        db = firestore.Client.from_service_account_json(key_file)
    else:
        print("Service account key not found.")
        return

    json_path = 'c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json'
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Syncing {len(data)} records to Firestore 'draws' collection...")
    
    batch = db.batch()
    count = 0
    for record in data:
        doc_id = record['date']
        doc_ref = db.collection('draws').document(doc_id)
        batch.set(doc_ref, record)
        count += 1
        
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Committed {count} records")

    batch.commit()
    print(f"Finished syncing {count} records.")

if __name__ == "__main__":
    sync_data()
