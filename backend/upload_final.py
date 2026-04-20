import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def initialize_firebase(service_account_path=None):
    """
    Initializes Firebase Admin SDK using either a service account key or Application Default Credentials.
    """
    if not firebase_admin._apps:
        if service_account_path and os.path.exists(service_account_path):
            print(f"Using service account key from: {service_account_path}")
            cred = credentials.Certificate(service_account_path)
        else:
            print("Using Application Default Credentials (ADC).")
            try:
                cred = credentials.ApplicationDefault()
            except Exception as e:
                print(f"Failed to load ADC: {e}")
                print("Please ensure you are logged in via 'gcloud auth application-default login' or provide a service account key.")
                return None
                
        firebase_admin.initialize_app(cred, {
            'projectId': 'ak-analysis-system-umair',
        })
    return firestore.client()

def upload_from_json(json_file):
    db = initialize_firebase()
    if not db:
        return

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        records = json.load(f)

    print(f"Starting upload of {len(records)} records to 'draws' collection...")
    
    batch = db.batch()
    count = 0
    uploaded_count = 0
    
    for r in records:
        # Use date as the document ID to prevent duplicates
        doc_id = r['date']
        doc_ref = db.collection('draws').document(doc_id)
        
        # Add a timestamp if missing
        if 'timestamp' not in r:
            r['timestamp'] = datetime.now().isoformat()
            
        batch.set(doc_ref, r)
        count += 1
        uploaded_count += 1
        
        # Firestore batches are limited to 500 operations
        if count >= 400:
            batch.commit()
            print(f"Committed batch. Total uploaded: {uploaded_count}")
            batch = db.batch()
            count = 0
            
    if count > 0:
        batch.commit()
        print(f"Committed final batch. Total uploaded: {uploaded_count}")
        
    print("\n[V] Data ingestion complete!")

if __name__ == "__main__":
    # Path to the deduplicated records file
    DATA_FILE = 'backend/records_to_upload.json'
    upload_from_json(DATA_FILE)
